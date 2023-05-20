import random
from datetime import datetime
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render

def lista_videos(request):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    published_before = datetime(year=2016, month=1, day=1).isoformat() + 'Z'
    youtube_request = youtube.search().list(
        part='snippet',
        type='video',
        maxResults=10,
        order='date',
        publishedBefore=published_before,
        q=''
    )
    response = youtube_request.execute()
    videos = response.get('items', [])
    random.shuffle(videos)
    videos = videos[:10]  # Limitamos a 10 vídeos por página

    context = {'videos': videos}
    return render(request, 'lista_videos.html', context)

def search_videos(request):
    query = request.GET.get('q', '')  # Obtém o valor da consulta de pesquisa da URL
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    published_before = datetime(year=2016, month=1, day=1).isoformat() + 'Z'
    youtube_request = youtube.search().list(
        part='snippet',
        type='video',
        maxResults=10,
        order='date',
        publishedBefore=published_before,
        q=query
    )
    response = youtube_request.execute()
    videos = response.get('items', [])
    
    context = {'videos': videos, 'query': query}
    return render(request, 'search_videos.html', context)

def video_player(request, video_id):
    context = {
        'video_id': video_id
    }
    return render(request, 'player.html', context)
