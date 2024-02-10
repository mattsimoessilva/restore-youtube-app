from django.contrib import admin
from .models import Tag, Channel, Video

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)
