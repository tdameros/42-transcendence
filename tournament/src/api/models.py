from django.db import models

from tournament import settings


class Tournament(models.Model):
    CREATED = 0
    IN_PROGRESS = 1
    FINISHED = 2

    name = models.CharField(max_length=settings.MAX_TOURNAMENT_NAME_LENGTH)
    max_players = models.IntegerField(default=16, blank=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    status = models.IntegerField(default=CREATED)
    admin_id = models.BigIntegerField(default=0)
