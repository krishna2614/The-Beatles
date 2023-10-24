from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    userId = models.CharField(max_length=10, unique=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return str(self.firstName) + ' ' + str(self.lastName)

    USERNAME_FIELD = 'userId'