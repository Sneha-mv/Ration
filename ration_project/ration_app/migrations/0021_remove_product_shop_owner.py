# Generated by Django 4.2.17 on 2024-12-10 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0020_product_shop_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shop_owner',
        ),
    ]