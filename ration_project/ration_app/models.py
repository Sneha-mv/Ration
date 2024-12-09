from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# For all
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('shop_owner', 'Shop Owner'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


# Shop Owner
class ShopOwnerDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_image = models.ImageField(upload_to='aadhar_images/')

    shop_name = models.CharField(max_length=100)
    shop_address = models.TextField()
    shop_license_number = models.CharField(max_length=50)
    license_image = models.ImageField(upload_to='license_images/')

    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.shop_name
    

CATEGORY_CHOICES = [
    ('APL', 'APL'),
    ('BPL', 'BPL'),
    ('AAY', 'AAY'),
    ('PHH', 'PHH'),
]

class Product(models.Model):
    shop_owner = models.ForeignKey(ShopOwnerDetails, on_delete=models.CASCADE, related_name='products',  null=True, blank=True) 
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    quantity = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

# User Section
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=False, default='0000000000')
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    address = models.TextField()
    ration_card_number = models.CharField(max_length=50)
    ration_card_image = models.ImageField(upload_to='ration_cards/', default='ration_cards/default.jpg')
    phone_number = models.CharField(max_length=15)
    booking_date = models.DateField()
    ration_shop = models.ForeignKey(ShopOwnerDetails, on_delete=models.SET_NULL, null=True, blank=True)
   
    def __str__(self):
        return f"Booking by {self.user.username} on {self.booking_date}"


