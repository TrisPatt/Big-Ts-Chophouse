# Generated by Django 4.2.14 on 2024-08-14 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
