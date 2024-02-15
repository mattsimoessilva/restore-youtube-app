from django.urls import path, include, re_path
from meu_aplicativo.views import search_videos, lista_videos, channel_page, video_player, RegisterView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/video/', search_videos, name='search_videos'),
    path('', lista_videos, name='lista_videos'),
    path('video_player/<str:video_id>/<str:channel_id>', video_player, name='video_player'),
    path('channel/<str:channel_id>/', channel_page, name='channel_page'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path(r'', include('pwa.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

