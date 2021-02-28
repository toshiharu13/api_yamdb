from rest_framework import serializers


from .models import Category, Comment, Genre, Review, Title, User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id', )




class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id', )


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    #rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('name', 'year', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)
    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'rating')
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
        existы = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if existы and self.context['request'].method == 'POST':
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
