# Generated by Django 4.2.17 on 2024-12-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]