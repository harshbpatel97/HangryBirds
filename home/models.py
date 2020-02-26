from django.db import models


# Create your models here.

class UserTable(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username
