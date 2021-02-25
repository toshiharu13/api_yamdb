from rest_framework import serializers

from .models import Titles, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('category', 'genre', 'description', 'name', 'year')
        model = Titles
