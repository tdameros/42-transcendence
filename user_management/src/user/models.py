import pyotp
from django.db import models

from user_management import settings


class User(models.Model):
    username = models.CharField(max_length=settings.USERNAME_MAX_LENGTH, unique=True)
    password = models.CharField(max_length=settings.PASSWORD_MAX_LENGTH, null=True)
    email = models.EmailField(max_length=settings.EMAIL_MAX_LENGTH, unique=True)
    emailVerified = models.BooleanField(default=False)
    emailVerificationToken = models.CharField(null=True, max_length=settings.EMAIL_VERIFICATION_TOKEN_MAX_LENGTH)
    emailVerificationTokenExpiration = models.DateTimeField(null=True)
    forgotPasswordCode = models.CharField(null=True, max_length=settings.FORGOT_PASSWORD_CODE_MAX_LENGTH)
    forgotPasswordCodeExpiration = models.DateTimeField(null=True)
    avatar = models.ImageField(null=True, upload_to='avatars/')
    has_2fa = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=settings.TOTP_SECRET_MAX_LENGTH, null=True)
    totp_config_url = models.CharField(max_length=settings.TOTP_CONFIG_URL_MAX_LENGTH, null=True)
    account_deleted = models.BooleanField(default=False)

    def verify_2fa(self, code):
        return pyotp.TOTP(self.totp_secret).verify(code)


class PendingOAuth(models.Model):
    hashed_state = models.CharField(max_length=settings.OAUTH_STATE_MAX_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=settings.OAUTH_SOURCE_MAX_LENGTH)


class Friend(models.Model):
    PENDING = 0
    ACCEPTED = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    status = models.IntegerField(default=PENDING)
