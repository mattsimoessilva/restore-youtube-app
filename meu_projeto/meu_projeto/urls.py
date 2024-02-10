from django.urls import path, include, re_path
from meu_aplicativo.views import lista_movies, search_movies, movie_player, company_page, load_more_movies, show_page, episode_player, search_videos, lista_videos, channel_page, video_player, mark_as_watched, mark_as_not_watched, lista_info
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_movies, name='search_movies'),
    path('search/video/', search_videos, name='search_videos'),
    path('', lista_movies, name='lista_movies'),
    path('videos/history/', lista_videos, name='lista_videos'),
    path('videos/computing/', lista_info, name='lista_info'),
    path('player/<str:movie_id>/', movie_player, name='movie_player'),
    path('video_player/<str:video_id>/', video_player, name='video_player'),
    path('episode_player/<str:episode_id>/', episode_player, name='episode_player'),
    path('company/<int:company_id>/', company_page, name='channel_page'),
    path('show/<int:show_id>/', show_page, name='show_page'),
    path('channel/<int:channel_id>/', channel_page, name='channel_page'),
    path('load_more_movies/', load_more_movies, name='load_more_movies'),
    path('mark_as_watched/<str:video_id>//', mark_as_watched, name='mark_as_watched'),
    path('mark_as_not_watched/<str:video_id>/', mark_as_not_watched, name='mark_as_not_watched'),
    re_path(r'', include('pwa.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

