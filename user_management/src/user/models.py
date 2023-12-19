from django.db import models

from user_management.src.user_management import settings


class User(models.Model):
    username = models.CharField(max_length={settings.USERNAME_MAX_LENGTH})
    elo = models.IntegerField(default={settings.DEFAULT_ELO})
    password = models.CharField(max_length={settings.PASSWORD_MAX_LENGTH})
    email = models.EmailField()
