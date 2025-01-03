# Generated by Django 4.2.17 on 2024-12-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0023_booking_payment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RationCardApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_of_the_house', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('punchayath_or_corporation', models.CharField(max_length=100)),
                ('ward_number', models.CharField(max_length=10)),
                ('house_number', models.CharField(max_length=20)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_family_members', models.IntegerField()),
                ('family_details', models.TextField()),
                ('id_proofs', models.FileField(blank=True, null=True, upload_to='id_proofs/')),
                ('date', models.DateField()),
            ],
        ),
    ]
