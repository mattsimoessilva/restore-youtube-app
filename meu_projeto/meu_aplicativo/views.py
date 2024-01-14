from random import sample
from django.shortcuts import get_object_or_404, render
from .models import Video, Channel
from datetime import datetime
from django.db.models import Q
import random
from random import sample
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.db.models import Count
from django.db.models import Q
from random import shuffle

def video_player(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Retrieve similar videos based on common tags
    similar_videos = Video.objects.filter(
        tags__in=video.tags.all()  # Get videos that share at least one tag
    ).exclude(id=video.id)  # Exclude the current video

    # Shuffle the list of similar videos to display them in a random order
    similar_videos = similar_videos.order_by('?')[:3]

    # Use a set to ensure uniqueness and convert back to a list
    unique_similar_videos = list(set(similar_videos))

    context = {
        'video': video,
        'titulo': video.title,
        'similar_videos': unique_similar_videos,
    }
    return render(request, 'player.html', context)

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
    Retrieve random videos from the database and render them on the 'lista_videos' template.
    """
    # Retrieve all videos from the database
    all_videos = Video.objects.all()

    # Get a random sample of videos (up to the number of available videos)
    random_videos = sample(list(all_videos), min(12, len(all_videos)))

    # Shuffle the list of random videos to display them in a random order
    random.shuffle(random_videos)

    titulo = "Em Destaque"
    context = {
        'videos': random_videos,
        'titulo': titulo,
    }
    return render(request, 'lista_videos.html', context)

def search_videos(request):
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter

    # Use Q objects to search for videos where title, channel name, or tags contain the query
    videos = Video.objects.filter(
        Q(title__icontains=query) |
        Q(channel__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    # Convert the videos queryset to a list
    videos_list = list(videos)

    # Randomly shuffle the list of videos
    shuffle(videos_list)  # Shuffle the list directly

    context = {'videos': videos_list, 'query': query, 'titulo': 'Pesquisar'}
    return render(request, 'search_videos.html', context)


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







