from django.db import models

class PreUser(models.Model):
    email = models.CharField(max_length=50)
    confirmation_code = models.CharField(max_length=50)

    def __str__(self):
        return self.email
