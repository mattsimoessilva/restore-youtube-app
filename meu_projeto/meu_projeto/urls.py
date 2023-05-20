from django.urls import path
from meu_aplicativo.views import lista_videos, search_videos, video_player
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('search/', search_videos, name='search_videos'),
    path('videos/', lista_videos, name='lista_videos'),
    path('player/<str:video_id>/', video_player, name='video_player'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
