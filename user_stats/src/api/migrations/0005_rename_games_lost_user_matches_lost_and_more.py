# Generated by Django 4.2.7 on 2024-01-31 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_match_user_matches_played_alter_match_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="games_lost",
            new_name="matches_lost",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="games_played",
            new_name="matches_played",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="games_won",
            new_name="matches_won",
        ),
    ]