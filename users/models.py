# users/models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_location = models.CharField(max_length=255, db_index=True)
    farm_size = models.FloatField()

    def __str__(self):
        return self.user.username
