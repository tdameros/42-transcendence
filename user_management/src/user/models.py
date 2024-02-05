from django.db import models

from user_management import settings


class User(models.Model):
    username = models.CharField(max_length=settings.USERNAME_MAX_LENGTH, unique=True)
    password = models.CharField(max_length=settings.PASSWORD_MAX_LENGTH, null=True)
    email = models.EmailField(max_length=settings.EMAIL_MAX_LENGTH, unique=True)
    forgotPasswordCode = models.CharField(null=True, max_length=settings.FORGOT_PASSWORD_CODE_MAX_LENGTH)
    forgotPasswordCodeExpiration = models.DateTimeField(null=True)
    avatar = models.ImageField(null=True, upload_to='avatars/')


class PendingOAuth(models.Model):
    hashed_state = models.CharField(max_length=settings.OAUTH_STATE_MAX_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=settings.OAUTH_SOURCE_MAX_LENGTH)
