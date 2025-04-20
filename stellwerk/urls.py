from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_dispatcher, name='home_dispatcher'),

]
