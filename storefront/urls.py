# storefront/urls.py
from django.urls import path

from stellwerk.views import home_dispatcher
from . import views

app_name = 'store_customer'

urlpatterns = [
    path('', home_dispatcher, name='home_dispatcher'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('login/', views.store_customer_login, name='store_customer_login'),
    path('register/', views.store_customer_register, name='store_customer_register'),
    path('logout/', views.store_customer_logout, name='store_customer_logout'),
]
