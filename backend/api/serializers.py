from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Genre, Movie, Review, WatchlistItem, Favorite


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MovieSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, allow_blank=True)
    genre_id = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_year', 'poster_url', 'genre', 'genre_name', 'average_score']

    def get_average_score(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        return round(sum(r.score for r in reviews) / reviews.count(), 1)


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'user', 'movie', 'text', 'score', 'created_at']
        read_only_fields = ['user', 'movie', 'created_at']


class WatchlistItemSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = WatchlistItem
        fields = ['id', 'movie', 'movie_title', 'status', 'added_at']
        read_only_fields = ['added_at']


class FavoriteSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'movie_title', 'created_at']
        read_only_fields = ['created_at']