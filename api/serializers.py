from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Titles, Category, Genre, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('search',)
        model = Genre

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User