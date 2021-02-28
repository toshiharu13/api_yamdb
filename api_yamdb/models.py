from django.db import models

'''from django.core.validators import MaxValueValidator, MinValueValidator


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
'''