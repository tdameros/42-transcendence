from django.db import models

from user_stats import settings


class User(models.Model):
    elo = models.IntegerField(default=settings.ELO_DEFAULT)
    games_played = models.IntegerField(default=settings.GAMES_PLAYED_DEFAULT)
    games_won = models.IntegerField(default=settings.GAMES_WON_DEFAULT)
    games_lost = models.IntegerField(default=settings.GAMES_LOST_DEFAULT)
    win_rate = models.FloatField(default=settings.WIN_RATE_DEFAULT)
    friends = models.IntegerField(default=settings.FRIENDS_DEFAULT)
