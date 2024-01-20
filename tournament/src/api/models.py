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
    password = models.CharField(max_length=settings.HASH_PASSWORD_MAX_LENGTH, blank=True, null=True)


class Player(models.Model):
    nickname = models.CharField(max_length=settings.MAX_NICKNAME_LENGTH)
    user_id = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='players')


class Match(models.Model):
    player_1 = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='player_1')
    player_2 = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='player_2')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
