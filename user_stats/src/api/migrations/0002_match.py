# Generated by Django 4.2.7 on 2024-01-29 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_score", models.IntegerField()),
                ("opponent_score", models.IntegerField()),
                ("result", models.BooleanField()),
                ("user_elo", models.IntegerField()),
                ("user_elo_delta", models.IntegerField()),
                ("user_win_rate", models.FloatField()),
                ("user_expected_result", models.FloatField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "opponent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="opponent",
                        to="api.user",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user",
                        to="api.user",
                    ),
                ),
            ],
        ),
    ]
