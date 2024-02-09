from random import sample
from django.shortcuts import get_object_or_404, render, redirect
from .models import Movie, Company, Tag, Show, Episode
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
from .models import Show, Episode, Video, Channel

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

def channel_page(request, channel_id):

    channel = get_object_or_404(Channel, id=channel_id)

    videos = Video.objects.filter(channel=channel)

    first_video = videos.first

    context = {
        'first_video': first_video,
        'channel': channel,
        'videos': videos,
    }

    return render(request, 'channel_page.html', context)

def load_more_movies(request):
    # Get the page number from the AJAX request
    page = int(request.GET.get('page', 1))
    movies_per_page = 12

    # Use Django's Paginator to handle pagination
    all_movies = Movie.objects.all()
    print(len(all_movies))
    paginator = Paginator(all_movies, movies_per_page)

    # Get the movies for the requested page
    while True:
        try:
            movies = paginator.page(page)
            if movies:
                break
            else:
                page += 1
        except EmptyPage:
            # If the page is out of range, return an empty list
            movies = []
            break

    # Serialize the movies to JSON
    movie_data = [{'title': movie.title, 'thumbnail': movie.thumbnail, 'url': reverse('movie_player',  args=[movie.id]), 'company_url': reverse('company_page', args=[movie.company.id]), 'company': movie.company.name, 'published_date': movie.published_date} for movie in movies]

    # Return the movie data as JSON response
    return JsonResponse({'movies': movie_data})


def lista_movies(request):
    """
    Retrieve random movies and shows for a sample of tags from the database and render them on the 'lista_movies' template.
    """
    # Retrieve all tags from the database
    all_tags = Tag.objects.all()

    # Get a random sample of tags (up to the number of available tags)
    random_tags = sample(list(all_tags), min(5, len(all_tags)))  # Change '5' to the desired number of random tags

    # Initialize an empty list to store movies and shows for each tag
    content_by_tags = []

    for tag in random_tags:
        # Retrieve all movies and shows for the current tag
        tag_movies = Movie.objects.filter(tags=tag)  # Assuming you have a 'tags' field in your Movie model
        tag_shows = Show.objects.filter(tags=tag)  # Assuming you have a 'tags' field in your Show model

        if tag_movies or tag_shows:
            # Get a random sample of movies and shows (up to the number of available movies and shows for this tag)
            tag_content_sample = sample(list(tag_movies) + list(tag_shows), min(8, len(tag_movies) + len(tag_shows)))
            # Shuffle the list of random movies and shows to display them in a random order
            shuffle(tag_content_sample)
            content_by_tags.append({
                'tag_name': tag.name,  # Assuming your Tag model has a 'name' field
                'content': tag_content_sample,
            })

    # Retrieve all movies and shows from the database
    all_movies = Movie.objects.all()
    all_shows = Show.objects.all()

    # Get a random sample of movies and shows (up to the number of available movies and shows)
    random_content = sample(list(all_movies) + list(all_shows), min(8, len(all_movies) + len(all_shows)))

    # Select a random movie or show from the list
    random_movie_or_show = choice(list(all_movies) + list(all_shows))

    # Shuffle the list of random movies and shows to display them in a random order
    shuffle(random_content)

    titulo = "Em Destaque"
    context = {
        'random_movie': random_movie_or_show,
        'movies': random_content,
        'titulo': titulo,
        'content_by_tags': content_by_tags,  # Include the movies and shows grouped by tags
    }

    print(content_by_tags)

    return render(request, 'lista_movies.html', context)

def lista_videos(request):

    all_videos = list(Video.objects.all())

    random_videos = sample(all_videos, min(8, len(all_videos)))

    shuffle(random_videos)

    titulo = "Em Destaque"
    context = {
        'videos': random_videos,
    }

    return render(request, 'lista_videos.html', context)

def search_movies(request):
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter

    # Use Q objects to search for movies and shows where title, channel name, or tags contain the query
    movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(company__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    shows = Show.objects.filter(
        Q(title__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    # Convert the movies and shows querysets to lists
    movies_list = list(movies)
    shows_list = list(shows)

    # Combine the lists of movies and shows
    content_list = movies_list + shows_list

    # Randomly shuffle the list of movies and shows
    shuffle(content_list)  # Shuffle the list directly

    context = {'content': content_list, 'query': query, 'titulo': 'Pesquisar'}
    return render(request, 'search_movies.html', context)

def search_videos(request):
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter

    movies = Video.objects.filter(
        Q(title__icontains=query) |
        Q(channel__title__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    videos_list = list(movies)

    shuffle(videos_list) 

    context = {'content': videos_list, 'query': query}
    return render(request, 'search_videos.html', context)


def movie_player(request, movie_id):
    """
    Retrieve the movie object from the database based on the movie_id and render it on the 'player' template.
    """
    movie = get_object_or_404(Movie, id=movie_id)

    # Retrieve random similar movies from the database
    try:
        # Retrieve all movies excluding the current movie_id
        all_movies = Movie.objects.exclude(id=movie_id)

        # Get a random sample of movies (up to the number of available movies)
        similar_movies = sample(list(all_movies), min(3, len(all_movies)))
    except Exception as e:
        # In case of an error, set similar_movies to an empty list
        print(f'Error getting random similar movies: {e}')
        similar_movies = []

    context = {
        'url': movie.url,
        'titulo': movie.title,
        'similar_movies': similar_movies,
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

def video_player(request, video_id):

    video = get_object_or_404(Video, id=video_id)

    try:

        all_videos = Video.objects.exclude(id=video_id)

        similar_videos = sample(list(all_videos), min(3, len(all_videos)))
    except Exception as e:

        print(f'Error getting random similar videos: {e}')
        similar_videos = []

    context = {
        'video': video,
        'similar_videos': similar_videos,
    }
    return render(request, 'video_player.html', context)

def company_page(request, company_id):
    """
    Retrieve channel information and list of channel movies ordered by publishing date,
    and render them on the 'channel_page' template.
    """
    # Retrieve the channel object from the database based on the channel_id
    company = get_object_or_404(Company, id=company_id)

    # Retrieve the movies associated with the channel, ordered by publishing date
    company_movies = Movie.objects.filter(company=company).order_by('-published_date')

    context = {
        'company': company,
        'titulo': 'Canal',
        'movies': company_movies,
    }
    return render(request, 'company_page.html', context)

def mark_as_watched(request, video_id):

    video = get_object_or_404(Video, id=video_id)

    video.watched = True
    video.save()

    previous_path = request.META.get('HTTP_REFERER')
    return redirect(previous_path)

def mark_as_not_watched(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Update the watched status of the video
    video.watched = False
    video.save()

    previous_path = request.META.get('HTTP_REFERER')
    return redirect(previous_path)


