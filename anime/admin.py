from django.contrib import admin
from .models import Anime, UserAnime, Genre, Studio, Episode, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year']
    search_fields = ['name']


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'studio', 'year', 'episodes']
    search_fields = ['title']
    list_filter = ['studio', 'genres']
    filter_horizontal = ['genres']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['anime', 'number', 'title', 'duration_minutes']
    list_filter = ['anime']
    search_fields = ['anime__title', 'title']


@admin.register(UserAnime)
class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'status', 'rating']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'anime__title']
