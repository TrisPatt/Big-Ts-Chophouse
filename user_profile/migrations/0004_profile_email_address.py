# Generated by Django 4.2.14 on 2024-08-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_remove_profile_email_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
