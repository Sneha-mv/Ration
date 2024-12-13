# Generated by Django 4.2.17 on 2024-12-13 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0023_booking_payment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RationCardApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_of_the_house', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('punchayath_or_corporation', models.CharField(max_length=255)),
                ('ward_number', models.CharField(max_length=10)),
                ('house_number', models.CharField(max_length=10)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_family_members', models.IntegerField()),
                ('family_details', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='IDProofs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='id_proofs/')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_proofs', to='ration_app.rationcardapplications')),
            ],
        ),
    ]
