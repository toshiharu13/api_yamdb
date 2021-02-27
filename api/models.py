from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, default='noname')
    slug = models.CharField(max_length=200, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200, default='noname')
    slug = models.CharField(max_length=200, unique=True)


class Titles(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="titles_category")
    genre = models.ForeignKey(Genre, null=True, on_delete=models.CASCADE, related_name="titles_genre")
    description = models.TextField(null=True)
    name = models.CharField(verbose_name='Название пройзведения', max_length=200, blank=False)
    year = models.IntegerField('Дата публикации', null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True)
    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Reviews(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reviews = models.ForeignKey(
        Reviews, on_delete=models.CASCADE
    )
