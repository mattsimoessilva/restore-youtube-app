from django.urls import path
from meu_aplicativo.views import lista_videos, search_videos, video_player, channel_page, load_more_videos  # Import the channel_page view
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_videos, name='search_videos'),
    path('videos/', lista_videos, name='lista_videos'),
    path('player/<str:video_id>/', video_player, name='video_player'),
    path('channel/<int:channel_id>/', channel_page, name='channel_page'),
    path('load_more_videos/', load_more_videos, name='load_more_videos'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
