# Generated by Django 4.2.7 on 2024-02-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_notification_data_notification_owner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='data',
            field=models.IntegerField(null=True),
        ),
    ]