from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import StoreUser, StoreOwnerUser
from django.contrib.auth import authenticate

def customer_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user and isinstance(user, StoreUser):
            login(request, user)
            return redirect('storefront:home')  # customize for your store
        messages.error(request, 'Invalid login credentials')

    return render(request, 'storefront/login.html')


def owner_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user and isinstance(user, StoreOwnerUser):
            login(request, user)
            return redirect('store_admin:dashboard')
        messages.error(request, 'Invalid login credentials')

    return render(request, 'store_admin/login.html')
