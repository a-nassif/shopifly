from django.urls import path
from . import views

app_name = 'store_admin'

urlpatterns = [
    path('dashboard/', views.store_dashboard_view, name='store_dashboard'),
    path('settings/', views.store_settings_view, name='store_settings'),
    path('check-domain/', views.check_store_domain, name='check_store_domain'),
    path('customer/', views.store_customers, name='store_customers'),
    path('products/add/', views.store_products, name='store_products'),
    path('orders/', views.store_orders, name='store_orders'),
    path('login/', views.store_owner_login, name='store_owner_login'),
    path('logout/', views.store_owner_logout, name='store_owner_logout'),
    path('register/', views.store_owner_register, name='store_owner_register'),
]
