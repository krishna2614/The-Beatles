from django.db import models
from accounts.models import User
from django.db.models import JSONField


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restroom = JSONField()
