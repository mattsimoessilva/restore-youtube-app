from random import sample
from django.shortcuts import get_object_or_404, render
from .models import Video, Channel
from datetime import datetime
from django.db.models import Q
import random
from random import sample

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
    """
    Perform a database query to search for videos that match the user's query and render them on the 'search_videos' template.
    """
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter
    
    # Use Q objects to search for videos where title or channel name contains the query
    videos = Video.objects.filter(Q(title__icontains=query) | Q(channel__name__icontains=query))
    
    # Convert the videos queryset to a list
    videos_list = list(videos)
    
    # Randomly shuffle the list of videos
    random.shuffle(videos_list)
    
    context = {'videos': videos_list, 'query': query, 'titulo': 'Pesquisar'}
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
        'video': video,
        'titulo': video.title,
        'similar_videos': similar_videos,
    }
    return render(request, 'player.html', context)

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



