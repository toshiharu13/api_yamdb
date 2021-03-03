
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=200, default='noname', unique=True, verbose_name='Категория'
    )
    slug = models.SlugField(max_length=200, unique=True)


class Genre(models.Model):
    name = models.CharField(
        max_length=200, default='noname', verbose_name='Жанр')
    slug = models.SlugField(max_length=200, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[year_validator],
        verbose_name='год издания',
    )
    description = models.TextField(verbose_name='описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='titles',
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

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
