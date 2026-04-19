from django.urls import path
from .views import (
    login_view,
    logout_view,
    search_movies_view,
    toggle_favorite_view,
    GenreListAPIView,
    MovieListAPIView,
    MovieDetailAPIView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    WatchlistAPIView,
    WatchlistDetailAPIView,
    FavoriteListAPIView,
)

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),

    path('genres/', GenreListAPIView.as_view()),
    path('movies/', MovieListAPIView.as_view()),
    path('movies/search/', search_movies_view),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view()),

    path('movies/<int:movie_id>/reviews/', ReviewListCreateAPIView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view()),

    path('watchlist/', WatchlistAPIView.as_view()),
    path('watchlist/<int:pk>/', WatchlistDetailAPIView.as_view()),

    path('favorites/', FavoriteListAPIView.as_view()),
    path('favorites/toggle/', toggle_favorite_view),
]