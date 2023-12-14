from django.db import models
from enum import Enum


class Tournament(models.Model):
    CREATED = 0
    IN_PROGRESS = 1
    FINISHED = 2

    name = models.CharField(max_length=20)
    max_players = models.IntegerField(default=16)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    status = models.IntegerField(default=CREATED)
