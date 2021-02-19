from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)


class Titles(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="titles_category")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="titles_genre")
    description = models.TextField()
    name = models.CharField(verbose_name='Название пройзведения', max_length=200)
    year = models.DateField("Дата публикации", auto_now_add=False)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntergerField(validator=[MinValueValidator(1), MaxValueValidator(10)])


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reviews = model.ForeignKey(
        Reviews, on_delete=models.CASCADE
    )