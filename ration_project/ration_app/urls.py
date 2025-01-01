from django.urls import path
from .import views
 
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/',views.contact,name='contact'),
    
    # Admin Section
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shop-owners/', views.shop_owner_list, name='shop_owner_list'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('approve/<int:owner_id>/', views.approve_owner, name='approve_owner'),
    path('reject/<int:owner_id>/', views.reject_owner, name='reject_owner'),
    path('payments-list/', views.payment_list, name='payment_list'),
    path('ration-cards/', views.view_ration_cards, name='view_ration_cards'),
    path('ration-card/<int:id>/', views.manage_ration_card, name='manage_ration_card'),
    path('ration-card/delete/<int:id>/', views.delete_ration_card, name='delete_ration_card'),

    # Shop Owner Section
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop_details/', views.shop_details, name='shop_details'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders_in_shop/', views.orders_in_shop, name='orders_in_shop'),

    # User Section
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking/',views.booking, name='booking'),
    path('filter-products/', views.filter_products_by_category, name='filter_products'),
    path('booking-details/', views.booking_details, name='booking_details'),
    path('payment-details/',views.payment_details,name='payment_details'),
    path('payment-success/',views.payment_success,name='payment_success'),
    path('apply-ration-card/', views.apply_ration_card, name='apply_ration_card'),
]


