from django.contrib import admin
from .models import Channel, Video, Batch

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
@admin.register(Batch)
class BacthAdmin(admin.ModelAdmin):
    list_display = ('title',)
