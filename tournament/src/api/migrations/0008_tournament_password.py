# Generated by Django 4.2.7 on 2024-01-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]