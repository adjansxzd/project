from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Genre, Movie, Review, WatchlistItem, Favorite
from .serializers import (
    LoginSerializer,
    MovieSearchSerializer,
    GenreSerializer,
    MovieSerializer,
    ReviewSerializer,
    WatchlistItemSerializer,
    FavoriteSerializer,
)


# ---------------- FBV ----------------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'})
    except Exception:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_movies_view(request):
    serializer = MovieSearchSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    movies = Movie.objects.all()

    query = serializer.validated_data.get('query')
    genre_id = serializer.validated_data.get('genre_id')
    year = serializer.validated_data.get('year')

    if query:
        movies = movies.filter(title__icontains=query)

    if genre_id:
        movies = movies.filter(genre_id=genre_id)

    if year:
        movies = movies.filter(release_year=year)

    return Response(MovieSerializer(movies, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite_view(request):
    movie_id = request.data.get('movie')
    if not movie_id:
        return Response({'error': 'movie is required'}, status=status.HTTP_400_BAD_REQUEST)

    movie = get_object_or_404(Movie, id=movie_id)
    favorite = Favorite.objects.filter(user=request.user, movie=movie).first()

    if favorite:
        favorite.delete()
        return Response({'message': 'Removed from favorites', 'is_favorite': False})

    Favorite.objects.create(user=request.user, movie=movie)
    return Response({'message': 'Added to favorites', 'is_favorite': True})


# ---------------- CBV / APIView ----------------

class GenreListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class MovieListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class ReviewListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        movie = get_object_or_404(Movie, id=movie_id)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        if review.user != request.user:
            return Response({'error': 'You can edit only your own review'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        if review.user != request.user:
            return Response({'error': 'You can delete only your own review'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = WatchlistItem.objects.filter(user=request.user)
        serializer = WatchlistItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        movie_id = request.data.get('movie')
        status_value = request.data.get('status', 'want_to_watch')

        movie = get_object_or_404(Movie, id=movie_id)

        item, created = WatchlistItem.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'status': status_value}
        )

        if not created:
            item.status = status_value
            item.save()

        serializer = WatchlistItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchlistDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        item = get_object_or_404(WatchlistItem, pk=pk, user=request.user)
        serializer = WatchlistItemSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = get_object_or_404(WatchlistItem, pk=pk, user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)