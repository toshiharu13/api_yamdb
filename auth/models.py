from django.db import models

class PreUser(models.Model):
    mail = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.mail
