from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
