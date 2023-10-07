from random import sample
from django.shortcuts import get_object_or_404, render
from .models import Video
from datetime import datetime

def lista_videos(request):
    """
    Retrieve the latest videos from the database and render them on the 'lista_videos' template.
    """
    latest_videos = Video.objects.all().order_by('-id')[:10]  # Order by primary key in descending order
    titulo = "Em Destaque"
    context = {
        'videos': latest_videos,
        'titulo': titulo,
    }
    return render(request, 'lista_videos.html', context)

def search_videos(request):
    """
    Perform a database query to search for videos that match the user's query and render them on the 'search_videos' template.
    """
    query = request.GET.get('q', '')  # Get the user's search query from the URL parameter
    videos = Video.objects.filter(title__icontains=query)  # You can extend this to search in description or other fields
    context = {'videos': videos, 'query': query, 'titulo': 'Pesquisar'}
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
        similar_videos = sample(list(all_videos), min(10, len(all_videos)))
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


