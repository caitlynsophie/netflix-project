from django.contrib import admin
from .models import NetflixTitle

@admin.register(NetflixTitle)
class NetflixTitleAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_type', 'release_year', 'rating']
    list_filter = ['title_type', 'release_year', 'rating']
    search_fields = ['title', 'cast', 'director']