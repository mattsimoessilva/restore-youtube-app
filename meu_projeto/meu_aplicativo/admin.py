from django.contrib import admin
from .models import Video, Channel

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'url')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'background_image_url')
