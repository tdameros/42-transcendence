from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    elo = models.IntegerField(default=500)
