from django.db import models

from user_management import settings


class User(models.Model):
    username = models.CharField(max_length=settings.USERNAME_MAX_LENGTH, unique=True)
    elo = models.IntegerField(default=settings.ELO_DEFAULT)
    password = models.CharField(max_length=settings.PASSWORD_MAX_LENGTH)
    email = models.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
