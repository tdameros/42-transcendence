# Generated by Django 4.2.7 on 2024-01-26 20:05

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo', models.IntegerField(default=500)),
                ('games_played', models.IntegerField(default=0)),
                ('games_won', models.IntegerField(default=0)),
                ('games_lost', models.IntegerField(default=0)),
                ('win_rate', models.FloatField(default=0.0)),
                ('friends', models.IntegerField(default=0)),
            ],
        ),
    ]
