# Generated by Django 4.2.7 on 2024-02-05 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_rename_games_lost_user_matches_lost_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="user_friends",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="match",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="api.user",
            ),
        ),
    ]
