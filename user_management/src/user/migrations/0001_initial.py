# Generated by Django 4.2.7 on 2024-03-04 14:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PendingOAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_state', models.CharField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('emailVerified', models.BooleanField(default=False)),
                ('emailVerificationToken', models.CharField(max_length=100, null=True)),
                ('emailVerificationTokenExpiration', models.DateTimeField(null=True)),
                ('forgotPasswordCode', models.CharField(max_length=6, null=True)),
                ('forgotPasswordCodeExpiration', models.DateTimeField(null=True)),
                ('avatar', models.ImageField(null=True, upload_to='avatars/')),
                ('has_2fa', models.BooleanField(default=False)),
                ('totp_secret', models.CharField(max_length=32, null=True)),
                ('totp_config_url', models.CharField(max_length=100, null=True)),
                ('account_deleted', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(null=True)),
                ('last_activity', models.DateTimeField(default=django.utils.timezone.now)),
                ('oauth', models.CharField(choices=[(None, 'None'), ('github', 'github'), ('42api', '42api')], default=None, max_length=7, null=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserOAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('github', 'github'), ('42api', '42api')], max_length=20)),
                ('service_id', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oauths', to='user.user')),
            ],
            options={
                'verbose_name': 'User OAuth',
                'verbose_name_plural': 'User OAuths',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='user.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.user')),
            ],
        ),
    ]
