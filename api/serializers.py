from rest_framework import serializers

from .models import Category, Comment, Genre, PreUser, Review, Title, User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


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
        queryset=Genre.objects.all(),
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        exist_or_not = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if exist_or_not and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на один объект.'
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


class PreUserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=50, required=False)

    class Meta:
        fields = ('email', 'confirmation_code')
        model = PreUser
