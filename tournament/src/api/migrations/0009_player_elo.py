# Generated by Django 4.2.7 on 2024-01-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_tournament_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='elo',
            field=models.IntegerField(null=True),
        ),
    ]