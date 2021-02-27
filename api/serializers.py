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


class TitleGetListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    category = serializers.SlugRelatedField(read_only=True,
                                            slug_field='slug',
                                            )
    genre = serializers.SlugRelatedField(read_only=True,
                                         slug_field='slug',
                                         #many=True,
                                         )

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'rating')
        model = Titles


class TitlesPostUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False,
    )
    year = serializers.IntegerField(
        required=False,
    )
    class Meta:
        fields = ('category', 'genre', 'description', 'name', 'year', 'id')
        model = Titles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User

