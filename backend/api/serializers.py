from rest_framework import serializers
from .models import Genre, Director, Movie, Review

# 1. Ручные сериализаторы (serializers.Serializer)

class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class DirectorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Director.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

# 2. Автоматические сериализаторы (serializers.ModelSerializer)

class MovieSerializer(serializers.ModelSerializer):
    # Добавляем вложенные данные, чтобы при запросе фильма выдавалось имя жанра и режиссера, а не просто их ID
    genre = GenreSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)
    
    # Эти поля используем для создания/обновления (передаем ID)
    genre_id = serializers.IntegerField(write_only=True)
    director_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'year', 'genre', 'director', 'genre_id', 'director_id']

class ReviewSerializer(serializers.ModelSerializer):
    # Добавляем имя пользователя, чтобы на фронтенде писать "Отзыв от Ivan"
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ['id', 'movie', 'author_username', 'text', 'rating']
        # Делаем так, чтобы автор не передавался с фронтенда, а брался из токена авторизации
        read_only_fields = ['author']