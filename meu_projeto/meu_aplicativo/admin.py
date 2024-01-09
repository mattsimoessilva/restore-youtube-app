from django.contrib import admin
from .models import Video, Channel, Tag, Show, Episode

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'url')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title',)
