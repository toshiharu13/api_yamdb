from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Titles, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('search',)
        model = Genre
