from django.contrib import admin
from .models import CustomUser, ShopOwnerDetails, Product, UserProfile, Booking, RationCardApplications, IDProofs
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ShopOwnerDetails)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(RationCardApplications)
admin.site.register(IDProofs)