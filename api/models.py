from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, default='noname', unique=True)
    slug = models.SlugField(max_length=200, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200, default='noname')
    slug = models.SlugField(max_length=200, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(
        null=True, db_index=True)
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name='titles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True)
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.CharField(max_length=9, choices=USER_ROLE, default=USER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=False,
        null=False
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )]


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )


class PreUser(models.Model):
    email = models.CharField(max_length=50)
    confirmation_code = models.CharField(max_length=50)

    def __str__(self):
        return self.email