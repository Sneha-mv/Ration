from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop_details/', views.shop_details, name='shop_details'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking/',views.booking, name='booking'),
]