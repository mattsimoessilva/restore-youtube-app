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
from .models import Video, Channel, Batch
from django.db.models import F
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
from django.db import transaction
import re

def channel_page(request, channel_id):
    
        channel = Channel.objects.get(id=channel_id)
    
        # Get videos without ordering
        videos = Video.objects.filter(channel_id=channel_id)

        # Parse 'uploadedDate' and sort videos in Python
        videos = sorted(videos, key=lambda video: parse_uploaded_date(video.uploadedDate))

        context = {
            'channel': channel,
            'videos': videos,
            'video_count': len(videos),
        }

        return render(request, 'channel_page.html', context)


def parse_uploaded_date(uploaded_date):
    if uploaded_date.startswith('Streamed'):
        # Extract the portion after 'Streamed'
        uploaded_date = uploaded_date[len('Streamed'):].strip()

    if 'ago' in uploaded_date:
        match = re.match(r'(\d+)\s+(\w+)', uploaded_date)
        if match:
            amount, unit = match.groups()
            amount = int(amount)
            
            # Handle both singular and plural forms
            if unit.endswith('s'):
                unit = unit[:-1]  # Remove 's' from the end
            
            if unit == 'year':
                return datetime.utcnow() - timedelta(days=365 * amount)
            elif unit == 'month':
                return datetime.utcnow() - timedelta(days=30 * amount)
            elif unit == 'week':
                return datetime.utcnow() - timedelta(weeks=amount)
            elif unit == 'day':
                return datetime.utcnow() - timedelta(days=amount)
            elif unit == 'hour':
                return datetime.utcnow() - timedelta(hours=amount)
            elif unit == 'minute':
                return datetime.utcnow() - timedelta(minutes=amount)
            elif unit == 'second':
                return datetime.utcnow() - timedelta(seconds=amount)

    # If the format doesn't match the expected 'ago' format, use dateutil.parser
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
        'videos': random_videos,
        'query': query,
    }

    # Return the shuffled videos as a rendered HTML response
    return render(request, 'search_videos.html', context)


def video_player(request, video_id, channel_id):
    
    video = Video.objects.get(id=video_id)
    videos = Video.objects.all().order_by('?')

    # Select a random sample of 24 videos
    random_videos = videos[:3]

    context = {
        'video': video,
        'videos': random_videos,
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

        max_retries = 10  # Adjust the number of retries as needed

        for attempt in range(max_retries):
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
                            print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                            time.sleep(10)
                            break  # Exit the loop on error

                    return videos

                else:
                    print(f"Error: {response.status_code}")
                    print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(10)
            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"Retrying in 60 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(60)

        # If all retries fail, raise an exception or return a default value
        raise Exception("Failed to fetch playlist data after multiple attempts")   

    def register_channel(self, channel_data):
        channel, created = Channel.objects.get_or_create(
            title=channel_data['title'],
            defaults={
                'logo': channel_data['logo'],
                'wallpaper': channel_data['wallpaper'],
                'description': channel_data['description'],
                'subscribers': channel_data['subscribers'],
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
                'duration': video_data['duration'],
                'views': video_data['views'],
            }
        )
        return video


    def register_playlist_data(self):
        playlist_id = Batch.objects.get(title='Study').playlist
        playlist_videos = self.fetch_playlist_data(playlist_id)
        consolidated_dict = {video['url']: video for sublist in playlist_videos for video in sublist}

        if consolidated_dict:
            # Get the latest processed batch number
            latest_batch_number = Batch.objects.latest('number').number if Batch.objects.exists() else 0

            # Increment the batch number for the new batch
            current_batch_number = latest_batch_number + 1
            
            videos_to_skip = current_batch_number

            # Skip videos from the beginning of the playlist
            playlist_videos = playlist_videos[videos_to_skip:]
            
            skipped_videos_len = 0
            for video in playlist_videos:
                skipped_videos_len += len(video)
            print(f'Quantide de vídeos cortados: {skipped_videos_len}')

            channel_list = []
            video_list = []

            # Experiment with different thread counts
            thread_count = 4  # Adjust this number based on your system and experimentation

            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                future_to_channel = {executor.submit(self.process_video_set, consolidated_dict[url]): url for url in consolidated_dict}

                for future in concurrent.futures.as_completed(future_to_channel):
                    videos = future_to_channel[future]

                    try:
                        results = future.result()
                        valid_results = [(channel, video) for channel, video in results if channel and video]
                        channel_list.extend([channel for channel, _ in valid_results])
                        video_list.extend([video for _, video in valid_results])
                        print(f"Successfully registered Videos from Playlist")
                    except Exception as e:
                        print(f"Error processing Playlist. Error: {e}")

            # Bulk save
            self.bulk_save(channel_list)
            self.bulk_save(video_list)

            if len(video_list) < len(consolidated_dict):
                print("Algo deu errado, número de vídeos cadastrados não é o mesmo da playlist")
                print(f'Tamanho do playlist_videos: {len(playlist_videos)}')
            elif len(video_list) >= len(consolidated_dict):
                print("Todos os vídeos cadastrados com sucesso")


    def process_video_set(self, video):
            results = []
            url = video.get('url', '')
            print(url)
            video_id = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('v', [''])[0]

            channel_url = video.get('uploaderUrl', '')
            this_channel_id = urllib.parse.urlparse(channel_url).path.lstrip("/channel/").split("?")[0]

            channel_data = self.fetch_channel_data(this_channel_id)

            print('BATATAAAAAAA')
            print(video)
            print('PIPOCAAAAAAAA')

            if video_id and channel_data:
                # Optimize URL parsing
                video_url = 'https://invidious.fdn.fr/embed/' + video_id
                thumbnail_url = 'https://img.youtube.com/vi/' + video_id + '/maxresdefault.jpg'

                channel_data = {
                    'title': channel_data.get('name', ''),
                    'logo': channel_data.get('avatarUrl', ''),
                    'wallpaper': channel_data.get('bannerUrl', ''),
                    'description': channel_data.get('description', ''),
                    'subscribers': channel_data['subscriberCount'],
                }

                # Batch channel and video operations
                channel = self.register_channel(channel_data)
                video_info = {
                    'title': video.get('title', ''),
                    'url': video_url,
                    'thumbnail': thumbnail_url,
                    'uploadedDate': video.get('uploadedDate', ''),
                    'duration': video['duration'],
                    'views': video['views'],
                }

                print(f'Video info: {video_info}')

                video_registration = self.register_video(video_info, channel)
                results.append((channel, video_registration))
            else:
                results.append((None, None))

            current_batch = Batch.objects.get()

            # Update the batch number
            current_batch.number = current_batch.number + 1
            current_batch.save()

            # Print the updated batch number
            print(f'Processed batch {current_batch.number}')
                
            return results

    def bulk_save(self, instances):
        # Perform bulk save operation
        for instance in instances:
            instance.save()
    
