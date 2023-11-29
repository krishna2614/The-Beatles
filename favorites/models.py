from django.db import models
from accounts.models import User
import jsonfield


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restroom_details = jsonfield.JSONField()
