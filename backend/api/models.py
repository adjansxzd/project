from django.contrib.auth.models import User
from django.db import models


class MovieManager(models.Manager):
    def recent(self):
        return self.filter(release_year__gte=2020)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    poster_url = models.URLField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')

    objects = models.Manager()
    recent_movies = MovieManager()

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class WatchlistItem(models.Model):
    STATUS_CHOICES = [
        ('want_to_watch', 'Want to watch'),
        ('watching', 'Watching'),
        ('watched', 'Watched'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_watch')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"