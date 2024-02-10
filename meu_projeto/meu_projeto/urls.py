from django.urls import path, include, re_path
from meu_aplicativo.views import search_videos, lista_videos, channel_page, video_player, mark_as_watched, mark_as_not_watched, lista_info
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/video/', search_videos, name='search_videos'),
    path('', lista_videos, name='lista_videos'),
    path('videos/computing/', lista_info, name='lista_info'),
    path('video_player/<str:video_id>/', video_player, name='video_player'),
    path('channel/<int:channel_id>/', channel_page, name='channel_page'),
    path('mark_as_watched/<str:video_id>//', mark_as_watched, name='mark_as_watched'),
    path('mark_as_not_watched/<str:video_id>/', mark_as_not_watched, name='mark_as_not_watched'),
    re_path(r'', include('pwa.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

