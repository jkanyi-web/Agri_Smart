from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  farm_location = models.CharField(max_length=255)
  farm_size = models.FloatField()

  def __str__(self):
      return self.user.username
  
