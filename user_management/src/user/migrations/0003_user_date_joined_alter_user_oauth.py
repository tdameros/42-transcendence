# Generated by Django 4.2.7 on 2024-03-03 22:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_oauth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='oauth',
            field=models.CharField(choices=[(None, 'None'), ('github', 'github'), ('42api', '42api')], default=None, max_length=7, null=True),
        ),
    ]
