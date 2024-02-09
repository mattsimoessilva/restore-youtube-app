from django.contrib import admin
from .models import Movie, Company, Tag, Show, Episode, Channel, Video

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'url')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
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

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)
