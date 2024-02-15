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
import requests
from django.shortcuts import render, get_object_or_404
from .models import Show, Episode, Video, Channel
from datetime import timedelta
from urllib.parse import urlparse, parse_qs
import json
import urllib.parse
import dateutil.parser 

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

   channel_api_url = f"https://api.piped.privacydev.net/channel/{channel_id}"

   playlist_id = "PLzkTtcbyuIZ8XFtDSXaS0QfqbT54wWC92"

   try:
       response = requests.get(channel_api_url)

       if response.status_code == 200:
            channel_info = response.json()
            playlist_videos = get_playlist_videos(playlist_id)

            videos = []
            for item in playlist_videos:
                for video in item:
                    duration_seconds = video.get('duration', 0)
                    
                    # Calculate duration in HH:MM:SS format
                    duration_formatted = str(timedelta(seconds=duration_seconds))

                    url = video.get('url', '')
                    parsed_url = urlparse(url)
                    video_id = parse_qs(parsed_url.query).get('v', [''])[0]

                    channel_url = video.get('uploaderUrl', '')
                    parsed_channel_url = urlparse(channel_url)
                    this_channel_id = parsed_channel_url.path.lstrip("/channel/").split("?")[0]

                    video_info = {
                        'duration': duration_seconds,
                        'duration_formatted': duration_formatted,
                        'thumbnail': video.get('thumbnail', ''),
                        'title': video.get('title', ''),
                        'uploadedDate': video.get('uploadedDate', ''),
                        'uploaderAvatar': video.get('uploaderAvatar', ''),
                        'uploaderUrl': video.get('uploaderUrl', ''),
                        'uploaderVerified': video.get('uploaderVerified', False),
                        'uploader': video.get('uploader', ''),
                        'url': url,
                        'video_id': video_id,
                        'channel_id': this_channel_id,
                        'views': video.get('views', 0),
                    }

                    if(video_info.get('channel_id') == channel_id):
                        videos.append(video_info)

            context = {
               'channel': channel_info,
               'videos': sorted(videos, key=lambda x: parse_uploaded_date(x['uploadedDate'])),
            }

            return render(request, 'channel_page.html', context)
       else:
           return JsonResponse({"error": f"API request failed with status code {response.status_code}"})
   except Exception as e:
       return JsonResponse({"error": f"An error occurred: {str(e)}"})


def parse_uploaded_date(uploaded_date):
    if 'years ago' in uploaded_date:
        years_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(days=365 * years_ago)
    elif 'months ago' in uploaded_date:
        months_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(days=30 * months_ago)
    elif 'days ago' in uploaded_date:
        days_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(days=days_ago)
    elif 'hours ago' in uploaded_date:
        hours_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(hours=hours_ago)
    elif 'minutes ago' in uploaded_date:
        minutes_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(minutes=minutes_ago)
    elif 'seconds ago' in uploaded_date:
        seconds_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(seconds=seconds_ago)
    else:
        return dateutil.parser.parse(uploaded_date)

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

def get_playlist_videos(playlist_id):
    base_url = "https://api.piped.privacydev.net/playlists/"
    

    url = f"{base_url}{playlist_id}"
    
    videos = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            playlist_info = response.json()
            videos.append(playlist_info.get("relatedStreams", []))
            next_page_token = response.json().get('nextpage')  # Initialize next_page_token

            token_list = []
            token_list.append(next_page_token)

            while next_page_token:  # Continue as long as there's a valid next_page_token
                next_base_url = "https://api.piped.privacydev.net/nextpage/playlists/"
                encoded_token = urllib.parse.quote(next_page_token, safe='')
                next_url = f"{next_base_url}{playlist_id}?nextpage={encoded_token}"
                
                print(f"Pupu: {next_url}")

                next_response = requests.get(next_url)

                if next_response.status_code == 200:
                    playlist_info = next_response.json()
                    videos.append(playlist_info.get("relatedStreams", []))
                    new_page_token = playlist_info.get('nextpage')
                    
                    if not new_page_token:  # Break out of the loop if no more tokens
                        break
                    
                    token_list.append(new_page_token)
                else:
                    print(f"Error fetching data from {next_url}")
                    break
            
            return videos

        else:
            print(f"Error: {response.status_code}")
            return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def lista_videos(request):
    playlist_id = "PLzkTtcbyuIZ8XFtDSXaS0QfqbT54wWC92"

    # Fetch videos from the random page
    playlist_videos = get_playlist_videos(playlist_id)
    
    print(playlist_videos[0])

    if not playlist_videos:
        return JsonResponse({"error": "Failed to fetch playlist videos"})

    # Extract video information from related streams
    videos = []
    channel_ids_seen = set()
    
    for item in playlist_videos:
        for stream in item:
            duration_seconds = stream.get('duration', 0)
            duration_formatted = str(timedelta(seconds=duration_seconds))

            url = stream.get('url', '')
            parsed_url = urlparse(url)
            video_id = parse_qs(parsed_url.query).get('v', [''])[0]

            channel_url = stream.get('uploaderUrl', '')
            parsed_channel_url = urlparse(channel_url)
            channel_id = parsed_channel_url.path.lstrip("/channel/").split("?")[0]

            video_info = {
                'duration': duration_seconds,
                'duration_formatted': duration_formatted,
                'thumbnail': stream.get('thumbnail', ''),
                'title': stream.get('title', ''),
                'uploadedDate': stream.get('uploadedDate', ''),
                'uploaderAvatar': stream.get('uploaderAvatar', ''),
                'uploaderUrl': stream.get('uploaderUrl', ''),
                'uploaderVerified': stream.get('uploaderVerified', False),
                'uploader': stream.get('uploader', ''),
                'url': url,
                'video_id': video_id,
                'channel_id': channel_id,
                'views': stream.get('views', 0),
            }

            if channel_id in channel_ids_seen and len(channel_ids_seen) >= 2:
                continue

            channel_ids_seen.add(channel_id)
            videos.append(video_info)
            print("Funfando...")

    # Shuffle the selected videos from the playlist
    shuffle(videos)

    # Select a random sample of 24 videos
    random_videos = videos[:24]

    context = {
        'videos': random_videos,
    }

    return render(request, 'lista_info.html', context)


def lista_info(request):
    # Retrieve videos with the "Computação" tag
    computacao_videos = Video.objects.filter(tags__name='Computação')

    # Randomly select up to 8 videos (or fewer if there are fewer than 8)
    random_videos = sample(list(computacao_videos), min(8, computacao_videos.count()))

    # Shuffle the selected videos
    shuffle(random_videos)

    context = {
        'videos': random_videos,
    }

    return render(request, 'lista_info.html', context)


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
            playlist_id = "PLzkTtcbyuIZ8XFtDSXaS0QfqbT54wWC92"

            # Fetch videos from the random page
            playlist_videos = get_playlist_videos(playlist_id)

            query = request.GET.get('q', '')
    
            videos = []
            for item in playlist_videos:
                for stream in item:
                    duration_seconds = stream.get('duration', 0)
                    
                    # Calculate duration in HH:MM:SS format
                    duration_formatted = str(timedelta(seconds=duration_seconds))

                    url = stream.get('url', '')
                    parsed_url = urlparse(url)
                    video_id = parse_qs(parsed_url.query).get('v', [''])[0]

                    channel_url = stream.get('uploaderUrl', '')
                    parsed_channel_url = urlparse(channel_url)
                    channel_id = parsed_channel_url.path.lstrip("/channel/").split("?")[0]

                    video_info = {
                        'duration': duration_seconds,
                        'duration_formatted': duration_formatted,
                        'thumbnail': stream.get('thumbnail', ''),
                        'title': stream.get('title', ''),
                        'uploadedDate': stream.get('uploadedDate', ''),
                        'uploaderAvatar': stream.get('uploaderAvatar', ''),
                        'uploaderUrl': stream.get('uploaderUrl', ''),
                        'uploaderVerified': stream.get('uploaderVerified', False),
                        'uploader': stream.get('uploader', ''),
                        'url': url,
                        'video_id': video_id,
                        'channel_id': channel_id,
                        'views': stream.get('views', 0),
                    }

                    query_low = query
                    title_low = stream.get("title", "").lower()

                    if query_low in title_low: 
                        videos.append(video_info)

            # Shuffle the selected videos from the playlist
            shuffle(videos)

            print(videos)

            # Select a random sample of 24 videos
            random_videos = videos[:24]

            context = {
                'content': videos,
                'query': query,
            }
            

            # Return the shuffled videos as a rendered HTML response
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

def video_player(request, video_id, channel_id):
    # Define the API endpoint for getting video information
    api_url = f"https://api.piped.privacydev.net/streams/{video_id}"
    url = f"https://piped.privacydev.net/embed/{video_id}"

    try:
        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            video_info = response.json()

            context = {
                'video': video_info,
                'url': url,
                'channel_id': channel_id,
            }

        

            return render(request, 'video_player.html', context)
        else:
            # Return an error response if the API request fails
            return JsonResponse({"error": f"API request failed with status code {response.status_code}"})
    except Exception as e:
        # Handle exceptions, such as network errors or JSON parsing errors
        return JsonResponse({"error": f"An error occurred: {str(e)}"})

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


