# Generated by Django 4.2.7 on 2024-03-02 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_user_id_from_42api_remove_user_id_from_github_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useroauth',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oauths', to='user.user'),
        ),
    ]
