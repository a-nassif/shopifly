# storefront/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.store_customer_login, name='store_customer_login'),
    path('register/', views.store_customer_register, name='store_customer_register'),
    path('logout/', views.store_customer_logout, name='store_customer_logout'),
]
