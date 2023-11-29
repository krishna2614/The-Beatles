from django.db import models
from accounts.models import User


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
