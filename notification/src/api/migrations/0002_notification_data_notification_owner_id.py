# Generated by Django 4.2.7 on 2024-02-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='data',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='owner_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
