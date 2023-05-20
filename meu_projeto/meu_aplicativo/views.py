import random
from datetime import datetime
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render
from config import API_KEY
import requests

def lista_videos(request):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
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
    youtube = build('youtube', 'v3', developerKey=API_KEY)
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
    # Fazer uma solicitação à API do YouTube para obter os detalhes do vídeo
    api_key = API_KEY
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    # Verificar se a resposta da API foi bem-sucedida
    if response.status_code == 200 and 'items' in data:
        # Extrair os detalhes do vídeo da resposta da API
        video_data = data['items'][0]
    else:
        # Em caso de falha na solicitação à API ou vídeo não encontrado, definir os valores como vazios
        video_data = {}

    similar_videos = get_similar_videos(video_id)

    context = {
        'video_id': video_id,
        'video_data': video_data,
        'similar_videos': similar_videos,
    }

    return render(request, 'player.html', context)

def get_similar_videos(video_id):
    # Configuração da API do YouTube
    api_key = API_KEY  # Substitua com sua própria chave de API do YouTube
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Define a data de referência como 1º de janeiro de 2016
        reference_date = datetime(2016, 1, 1).isoformat() + "Z"

        # Faz a chamada para a API do YouTube para obter vídeos relacionados
        response = youtube.search().list(
            part='snippet',
            type='video',
            relatedToVideoId=video_id,
            maxResults=5,  # Defina o número máximo de vídeos similares que você deseja obter
            publishedBefore=reference_date  # Filtra apenas vídeos publicados antes de 2016
        ).execute()

        # Extrai as informações relevantes dos vídeos similares
        similar_videos = []
        for item in response['items']:
            video = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'channel_name': item['snippet']['channelTitle'],
            }
            similar_videos.append(video)

        return similar_videos

    except HttpError as e:
        print(f'Erro ao buscar vídeos similares: {e}')
        return []