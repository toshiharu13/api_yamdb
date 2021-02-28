from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title, User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'rating', 'description')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        existos = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if existos and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Сорри, ошибочка('
                )
        return attrs

    class Meta:
        read_only_fields = ['id', 'title', 'pub_date', ]
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        read_only_fields = ['id', 'review', 'pub_date', ]
        fields = '__all__'
        model = Comment
