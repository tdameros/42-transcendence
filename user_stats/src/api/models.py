from django.db import models
from user_stats import settings


class User(models.Model):
    elo = models.IntegerField(default=settings.ELO_DEFAULT)
    matches_played = models.IntegerField(default=settings.MATCHES_PLAYED_DEFAULT)
    matches_won = models.IntegerField(default=settings.MATCHES_WON_DEFAULT)
    matches_lost = models.IntegerField(default=settings.MATCHES_LOST_DEFAULT)
    win_rate = models.FloatField(default=settings.WIN_RATE_DEFAULT)
    friends = models.IntegerField(default=settings.FRIENDS_DEFAULT)


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opponent')
    user_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    result = models.BooleanField(null=True)
    user_elo = models.IntegerField(null=True)
    user_win_rate = models.FloatField(null=True)
    user_matches_played = models.IntegerField(null=True)
    user_friends = models.IntegerField(null=True)
    user_elo_delta = models.IntegerField(null=True)
    user_expected_result = models.FloatField(null=True)
    date = models.DateTimeField(null=True)
