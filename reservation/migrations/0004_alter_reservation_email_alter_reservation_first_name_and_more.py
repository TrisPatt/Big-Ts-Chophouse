# Generated by Django 4.2.15 on 2024-08-18 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_reservation_email_alter_reservation_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]
