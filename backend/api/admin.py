from django.contrib import admin
from .models import Genre, Movie, Review, WatchlistItem, Favorite

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(WatchlistItem)
admin.site.register(Favorite)