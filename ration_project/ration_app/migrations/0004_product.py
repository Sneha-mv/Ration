# Generated by Django 4.2.17 on 2024-12-07 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0003_shopownerdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('APL', 'APL'), ('BPL', 'BPL'), ('AAY', 'AAY'), ('PHH', 'PHH')], max_length=3)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability', models.BooleanField(default=True)),
            ],
        ),
    ]