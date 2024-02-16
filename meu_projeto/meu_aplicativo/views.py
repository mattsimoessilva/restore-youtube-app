from random import sample
from django.shortcuts import get_object_or_404, render, redirect
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
from .models import Video, Channel
from datetime import timedelta
from urllib.parse import urlparse, parse_qs
import json
import urllib.parse
import dateutil.parser 
import time
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import concurrent.futures

def channel_page(request, channel_id):
    
        channel = Channel.objects.get(id=channel_id)
    
        # Get videos without ordering
        videos = Video.objects.filter(channel_id=channel_id)

        # Parse 'uploadedDate' and sort videos in Python
        videos = sorted(videos, key=lambda video: parse_uploaded_date(video.uploadedDate))

        context = {
            'channel': channel,
            'videos': videos,
        }

        return render(request, 'channel_page.html', context)


def parse_uploaded_date(uploaded_date):
    if 'years ago' in uploaded_date:
        years_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(days=365 * years_ago)
    elif 'months ago' in uploaded_date:
        months_ago = int(uploaded_date.split()[0])
        return datetime.utcnow() - timedelta(days=30 * months_ago)
    elif 'weeks ago' in uploaded_date:
            weeks_ago = int(uploaded_date.split()[0])
            return datetime.utcnow() - timedelta(weeks=weeks_ago)
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
                    print("Retrying in 5 seconds...")
                    time.sleep(10)  # Wait for 5 seconds before retrying

        return videos

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        return None

def lista_videos(request):
    
    videos = Video.objects.all().order_by('?')

    # Select a random sample of 24 videos
    random_videos = videos[:24]

    context = {
        'videos': random_videos,
    }

    return render(request, 'lista_info.html', context)


def search_videos(request):
    query = request.GET.get('q', '').lower()
    
    # Filter videos whose title contains the query
    videos = Video.objects.filter(title__icontains=query).order_by("?")
    
    # Select a random sample of 24 videos
    random_videos = videos[:20]

    context = {
        'content': random_videos,
        'query': query,
    }

    # Return the shuffled videos as a rendered HTML response
    return render(request, 'search_videos.html', context)


def video_player(request, video_id, channel_id):
    
    video = Video.objects.get(id=video_id)
    

    context = {
        'video': video,
    }

        

    return render(request, 'video_player.html', context)

class RegisterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Fetch and register channel and video data
        self.register_playlist_data()

        # You can add any additional logic or response here
        return JsonResponse({"message": "Registration process completed."})

    def fetch_channel_data(self, channel_id):
        base_url = "https://api.piped.privacydev.net/channel/"
        url = f"{base_url}{channel_id}"

        print(url)

        for _ in range(10):  # Retry up to 3 times
            try:
                response = requests.get(url)

                if response.status_code == 200:
                    channel_info = response.json()
                    return channel_info
                else:
                    print(f"Error: {response.status_code}")

            except Exception as e:
                print(f"An error occurred: {e}")

            # Wait for 10 seconds before retrying
            time.sleep(60)

        return None

    def fetch_playlist_data(self, playlist_id):
        base_url = "https://api.piped.privacydev.net/playlists/"
        url = f"{base_url}{playlist_id}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                playlist_info = response.json()
                videos = [playlist_info.get("relatedStreams", [])]
                next_page_token = playlist_info.get('nextpage')

                token_list = [next_page_token] if next_page_token else []

                while next_page_token:
                    next_base_url = "https://api.piped.privacydev.net/nextpage/playlists/"
                    encoded_token = urllib.parse.quote(next_page_token, safe='')
                    next_url = f"{next_base_url}{playlist_id}?nextpage={encoded_token}"

                    print(f"Fetching data from: {next_url}")

                    next_response = requests.get(next_url)

                    if next_response.status_code == 200:
                        playlist_info = next_response.json()
                        videos.append(playlist_info.get("relatedStreams", []))
                        next_page_token = playlist_info.get('nextpage')

                        if not next_page_token:
                            break

                        token_list.append(next_page_token)
                    else:
                        print(f"Error fetching data from {next_url}")
                        print("Retrying in 5 seconds...")
                        time.sleep(10)
                        break  # Exit the loop on error

                return videos

            else:
                print(f"Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            return None

    def register_channel(self, channel_data):
        channel, created = Channel.objects.get_or_create(
            title=channel_data['title'],
            defaults={
                'logo': channel_data['logo'],
                'wallpaper': channel_data['wallpaper'],
                'description': channel_data['description'],
            }
        )

        return channel

    def register_video(self, video_data, channel):
        video, created = Video.objects.get_or_create(
            title=video_data['title'],
            channel=channel,
            defaults={
                'url': video_data['url'],
                'thumbnail': video_data['thumbnail'],
                'uploadedDate': video_data['uploadedDate'],
            }
        )
        return video

    def register_playlist_data(self):
        playlist_id = "PLzkTtcbyuIZ8XFtDSXaS0QfqbT54wWC92"
        playlist_videos = self.fetch_playlist_data(playlist_id)

        if playlist_videos:
            channel_list = []
            video_list = []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_channel = {executor.submit(self.process_video_set, videos_set): videos_set for test in playlist_videos for videos_set in test}
                
                for future in concurrent.futures.as_completed(future_to_channel):
                    videos_set = future_to_channel[future]

                    try:
                        channel, video = future.result()
                        if channel and video:
                            channel_list.append(channel)
                            video_list.append(video)
                            print(f"Successfully registered Video: {video.title} from Channel: {channel.title}")
                        else:
                            print(f"Failed to register Video: {video.title} from Channel: {channel.title}")
                    except Exception as e:
                        print(f"Error processing Video Set: {videos_set}. Error: {e}")

            # Bulk save
            channels_saved = self.bulk_save(channel_list)
            videos_saved = self.bulk_save(video_list)

            for channel, video in zip(channels_saved, videos_saved):
                if channel and video:
                    print(f"Successfully registered Video: {video.title} from Channel: {channel.title}")
                else:
                    print(f"Failed to register Video: {video.title} from Channel: {channel.title}")

    def process_video_set(self, videos_set):
        url = videos_set.get('url', '')
        print(url)
        video_id = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('v', [''])[0]

        channel_url = videos_set.get('uploaderUrl', '')
        this_channel_id = urllib.parse.urlparse(channel_url).path.lstrip("/channel/").split("?")[0]

        channel_data = self.fetch_channel_data(this_channel_id)

        if video_id and channel_data:
            # Optimize URL parsing
            video_url = 'https://piped.privacydev.net/embed/' + video_id

            # Simplify channel_data handling
            channel_data['wallpaper'] = channel_data.get('bannerUrl', 'https://img.zcool.cn/community/03837b955deb1590000015995760355.jpg')

            print(channel_data)

            # Batch channel and video operations
            channel = self.register_channel(channel_data)
            video_info = {
                'title': videos_set.get('title', ''),
                'url': video_url,
                'thumbnail': videos_set.get('thumbnail', ''),
                'uploadedDate': videos_set.get('uploadedDate', ''),
            }
            video = self.register_video(video_info, channel)

            return channel, video
        else:
            return None, None

    # The rest of the class remains unchanged
