# Generated by Django 4.2.7 on 2024-01-26 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_match_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='player_1_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='player_2_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to='api.player'),
        ),
    ]
