from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    MovieListCreateView, MovieDetailView,
    GenreListView, ReviewListView, ReviewCreateView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('movies/', MovieListCreateView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('genres/', GenreListView.as_view()),
    path('reviews/', ReviewListView.as_view()),
    path('reviews/create/', ReviewCreateView.as_view()),
]