from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import viewsets, filters, permissions, mixins, status
from rest_framework.response import Response

from .models import Titles, Category, Genre
from .serializers import GenreSerializer, CategoriesSerializer, TitlesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def destroy(self, request, *args, **kwargs):
        genre = self.get_object()
        self.perform_destroy(genre)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()


# class TitlesViewSet(viewsets.ModelViewSet):
#     serializer_class = TitlesSerializer
#

