from django.contrib import admin
from .models import Channel, Video

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)
