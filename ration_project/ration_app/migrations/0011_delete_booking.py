# Generated by Django 4.2.17 on 2024-12-07 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0010_alter_userprofile_phone_number_booking'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]