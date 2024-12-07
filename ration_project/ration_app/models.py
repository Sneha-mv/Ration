from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# For all
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('shop_owner', 'Shop Owner'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


# Shop Owner
class ShopOwnerDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_image = models.ImageField(upload_to='aadhar_images/')

    shop_name = models.CharField(max_length=100)
    shop_address = models.TextField()
    shop_license_number = models.CharField(max_length=50)
    license_image = models.ImageField(upload_to='license_images/')

    def __str__(self):
        return self.shop_name
    
    # models.py
from django.db import models

CATEGORY_CHOICES = [
    ('APL', 'APL'),
    ('BPL', 'BPL'),
    ('AAY', 'AAY'),
    ('PHH', 'PHH'),
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    quantity = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

