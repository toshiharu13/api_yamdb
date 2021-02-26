from rest_framework import serializers

from .models import Titles, Category, Genre, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre



class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True)
    class Meta:
        fields = ('category', 'genre', 'description', 'name', 'year')
        model = Titles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User

