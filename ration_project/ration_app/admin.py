from django.contrib import admin
from .models import CustomUser, ShopOwnerDetails, Product
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ShopOwnerDetails)
admin.site.register(Product)