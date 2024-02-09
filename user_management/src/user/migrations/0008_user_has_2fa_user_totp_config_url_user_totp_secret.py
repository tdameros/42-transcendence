# Generated by Django 4.2.7 on 2024-02-04 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_pendingoauth_source_alter_user_forgotpasswordcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_2fa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='totp_config_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='totp_secret',
            field=models.CharField(max_length=32, null=True),
        ),
    ]