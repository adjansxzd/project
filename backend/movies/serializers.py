from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, Genre, Review, Profile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['user']

    def get_reviews(self, obj):
        return obj.reviews.values('rating')


class GenreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'movie', 'user', 'created_at']


class ReviewCreateSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    text = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=10)

    def validate_movie_id(self, value):
        if not Movie.objects.filter(id=value).exists():
            raise serializers.ValidationError('Movie not found')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        movie = Movie.objects.get(id=validated_data['movie_id'])
        return Review.objects.create(
            movie=movie,
            user=request.user if request else None,
            text=validated_data['text'],
            rating=validated_data['rating']
        )


class ProfileSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['avatar', 'movies_count']

    def get_movies_count(self, obj):
        return obj.user.movie_set.count()