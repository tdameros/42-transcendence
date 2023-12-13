from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=20)
    max_players = models.IntegerField(default=16)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
