from rest_framework import serializers

from .models import Category, Comment, Genre, Reviews, Titles, User


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
        fields = '__all__'
        model = Titles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment
