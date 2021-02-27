from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import ListPostDelMix
from .permissions import IsAdminOrNone, IsAdminOrRead, IsModeratorAdminAuthor


User = get_user_model()

from .models import Titles, Category, Genre
from .serializers import GenreSerializer, UserSerializer, CategoriesSerializer, TitlesPostUpdateSerializer, TitleGetListSerializer


from .models import Category, Comment, Genre, Reviews, Titles
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, ReviewsSerializer, TitlesSerializer,
                          UserSerializer)


class GenresViewSet(ListPostDelMix):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrRead]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(ListPostDelMix):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrRead]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    #  serializer_class = TitlesSerializer
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleGetListSerializer
        return TitlesPostUpdateSerializer
    queryset = Titles.objects.all()
    http_method_names = ('get', 'post', 'delete', 'patch')
    permission_classes = [IsAdminOrRead]


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PATCH'])
    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrNone]
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'delete', 'patch')
    lookup_field = 'username'


class ReviewsModelSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
