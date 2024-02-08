from random import sample
from django.shortcuts import get_object_or_404, render
from .models import Video, Channel, Tag, Show, Episode
from datetime import datetime
from django.db.models import Q
import random
from random import sample
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from random import choice, shuffle, sample
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Show, Episode

def show_page(request, show_id):
    """
    Retrieve a Show object and its associated Episodes from the database and render them on the 'show_page' template.
    """
    # Retrieve the Show object with the given id
    show = get_object_or_404(Show, id=show_id)

    # Retrieve all Episodes associated with this Show
    episodes = Episode.objects.filter(show=show)

    first_episode = episodes.first

    context = {
        'first_episode': first_episode,
        'show': show,
        'episodes': episodes,
    }

    return render(request, 'show_page.html', context)

def load_more_videos(request):
    # Get the page number from the AJAX request
    page = int(request.GET.get('page', 1))
    videos_per_page = 12

    # Use Django's Paginator to handle pagination
    all_videos = Video.objects.all()
    print(len(all_videos))
    paginator = Paginator(all_videos, videos_per_page)

    # Get the videos for the requested page
    while True:
        try:
            videos = paginator.page(page)
            if videos:
                break
            else:
                page += 1
        except EmptyPage:
            # If the page is out of range, return an empty list
            videos = []
            break

    # Serialize the videos to JSON
    video_data = [{'title': video.title, 'thumbnail': video.thumbnail, 'url': reverse('video_player',  args=[video.id]), 'channel_url': reverse('channel_page', args=[video.channel.id]), 'channel': video.channel.name, 'published_date': video.published_date} for video in videos]

    # Return the video data as JSON response
    return JsonResponse({'videos': video_data})


def lista_videos(request):
    """
    Retrieve random videos and shows for a sample of tags from the database and render them on the 'lista_videos' template.
    """
    # Retrieve all tags from the database
    all_tags = Tag.objects.all()

    # Get a random sample of tags (up to the number of available tags)
    random_tags = sample(list(all_tags), min(5, len(all_tags)))  # Change '5' to the desired number of random tags

    # Initialize an empty list to store videos and shows for each tag
    content_by_tags = []

    for tag in random_tags:
        # Retrieve all videos and shows for the current tag
        tag_videos = Video.objects.filter(tags=tag)  # Assuming you have a 'tags' field in your Video model
        tag_shows = Show.objects.filter(tags=tag)  # Assuming you have a 'tags' field in your Show model

        if tag_videos or tag_shows:
            # Get a random sample of videos and shows (up to the number of available videos and shows for this tag)
            tag_content_sample = sample(list(tag_videos) + list(tag_shows), min(8, len(tag_videos) + len(tag_shows)))
            # Shuffle the list of random videos and shows to display them in a random order
            shuffle(tag_content_sample)
            content_by_tags.append({
                'tag_name': tag.name,  # Assuming your Tag model has a 'name' field
                'content': tag_content_sample,
            })

    # Retrieve all videos and shows from the database
    all_videos = Video.objects.all()
    all_shows = Show.objects.all()

    # Get a random sample of videos and shows (up to the number of available videos and shows)
    random_content = sample(list(all_videos) + list(all_shows), min(8, len(all_videos) + len(all_shows)))

    # Select a random video or show from the list
    random_video_or_show = choice(list(all_videos) + list(all_shows))

    # Shuffle the list of random videos and shows to display them in a random order
    shuffle(random_content)

    titulo = "Em Destaque"
    context = {
        'random_video': random_video_or_show,
        'videos': random_content,
        'titulo': titulo,
        'content_by_tags': content_by_tags,  # Include the videos and shows grouped by tags
    }

    print(content_by_tags)

    return render(request, 'lista_videos.html', context)

def search_videos(request):
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter

    # Use Q objects to search for videos and shows where title, channel name, or tags contain the query
    videos = Video.objects.filter(
        Q(title__icontains=query) |
        Q(channel__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    shows = Show.objects.filter(
        Q(title__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    # Convert the videos and shows querysets to lists
    videos_list = list(videos)
    shows_list = list(shows)

    # Combine the lists of videos and shows
    content_list = videos_list + shows_list

    # Randomly shuffle the list of videos and shows
    shuffle(content_list)  # Shuffle the list directly

    context = {'content': content_list, 'query': query, 'titulo': 'Pesquisar'}
    return render(request, 'search_videos.html', context)


def video_player(request, video_id):
    """
    Retrieve the video object from the database based on the video_id and render it on the 'player' template.
    """
    video = get_object_or_404(Video, id=video_id)

    # Retrieve random similar videos from the database
    try:
        # Retrieve all videos excluding the current video_id
        all_videos = Video.objects.exclude(id=video_id)

        # Get a random sample of videos (up to the number of available videos)
        similar_videos = sample(list(all_videos), min(3, len(all_videos)))
    except Exception as e:
        # In case of an error, set similar_videos to an empty list
        print(f'Error getting random similar videos: {e}')
        similar_videos = []

    context = {
        'url': video.url,
        'titulo': video.title,
        'similar_videos': similar_videos,
    }
    return render(request, 'player.html', context)

def episode_player(request, episode_id):

    episode = get_object_or_404(Episode, id=episode_id)

    try:

        all_episodes = Episode.objects.exclude(id=episode_id)

        similar_episodes = sample(list(all_episodes), min(3, len(all_episodes)))
    except Exception as e:

        print(f'Error getting random similar episodes: {e}')
        similar_episodes = []

    context = {
        'url': episode.url,
        'titulo': episode.title,
        'similar_episodes': similar_episodes,
    }
    return render(request, 'episode_player.html', context)

def channel_page(request, channel_id):
    """
    Retrieve channel information and list of channel videos ordered by publishing date,
    and render them on the 'channel_page' template.
    """
    # Retrieve the channel object from the database based on the channel_id
    channel = get_object_or_404(Channel, id=channel_id)

    # Retrieve the videos associated with the channel, ordered by publishing date
    channel_videos = Video.objects.filter(channel=channel).order_by('-published_date')

    context = {
        'channel': channel,
        'titulo': 'Canal',
        'videos': channel_videos,
    }
    return render(request, 'channel_page.html', context)



