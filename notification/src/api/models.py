from django.db import models

from notification import settings


class Notification(models.Model):
    title = models.CharField(max_length=settings.TITLE_MAX_LENGTH)
    type = models.CharField(max_length=64)
    owner_id = models.IntegerField()
    data = models.IntegerField(null=True)
