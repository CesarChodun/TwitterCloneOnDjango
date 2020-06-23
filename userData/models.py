

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

# class UserDataManager(models.Manager):
#     def create_user_data:


class UserData(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    registration_date = models.DateTimeField('date of registration')

