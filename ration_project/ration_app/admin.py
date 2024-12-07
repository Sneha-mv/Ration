from django.contrib import admin
from .models import CustomUser, ShopOwnerDetails, Product, UserProfile
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ShopOwnerDetails)
admin.site.register(Product)
admin.site.register(UserProfile)
