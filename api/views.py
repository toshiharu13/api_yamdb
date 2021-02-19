from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, permissions, mixins

from .models import Titles, Category, Genre
from .serializers import GenreSerializer


class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
