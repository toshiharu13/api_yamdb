from django.db import models


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
