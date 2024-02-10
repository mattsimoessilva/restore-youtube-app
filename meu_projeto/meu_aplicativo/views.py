from random import sample
from django.shortcuts import get_object_or_404, render, redirect
from .models import  Tag
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
from .models import Video, Channel

def channel_page(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)

    # Order videos by release_date, older first
    videos = Video.objects.filter(channel=channel).order_by('published_date')

    first_video = videos.first()

    context = {
        'first_video': first_video,
        'channel': channel,
        'videos': videos,
    }

    return render(request, 'channel_page.html', context)

def lista_videos(request):
    # Retrieve videos with the "Computação" tag
    historia_videos = Video.objects.all()

    # Randomly select up to 8 videos (or fewer if there are fewer than 8)
    random_videos = sample(list(historia_videos), min(8, historia_videos.count()))

    # Shuffle the selected videos
    shuffle(random_videos)

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


