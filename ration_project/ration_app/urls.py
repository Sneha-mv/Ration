from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
     path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]