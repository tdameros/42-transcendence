from django.db import models

from user_stats import settings


class User(models.Model):
    elo = models.IntegerField(default=settings.ELO_DEFAULT)
    games_played = models.IntegerField(default=settings.GAMES_PLAYED_DEFAULT)
    games_won = models.IntegerField(default=settings.GAMES_WON_DEFAULT)
    games_lost = models.IntegerField(default=settings.GAMES_LOST_DEFAULT)
    win_rate = models.FloatField(default=settings.WIN_RATE_DEFAULT)
    friends = models.IntegerField(default=settings.FRIENDS_DEFAULT)


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opponent')
    user_score = models.IntegerField()
    opponent_score = models.IntegerField()
    result = models.BooleanField()
    user_elo = models.IntegerField()
    user_elo_delta = models.IntegerField()
    user_win_rate = models.FloatField()
    user_expected_result = models.FloatField()
    date = models.DateTimeField()
