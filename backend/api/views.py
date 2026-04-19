from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer

# ==========================================
# 1. FBV: Function-Based Views (Фильмы)
# ==========================================

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
        
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 2. CBV: Class-Based Views (Отзывы)
# ==========================================

class ReviewList(APIView):
    # Разрешаем читать всем, но создавать только авторизованным
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # ТРЕБОВАНИЕ: Привязка создаваемого объекта к request.user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated] # Только для авторизованных

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def delete(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Удалять можно только свои отзывы
        if review.author != request.user:
            return Response({"error": "You cannot delete this review."}, status=status.HTTP_403_FORBIDDEN)
            
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)