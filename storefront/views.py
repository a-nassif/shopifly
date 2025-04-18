from django.shortcuts import render

# Create your views here.

# storefront/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import StoreCustomerUser


def store_home(request):
    products = request.store.product_set.all()
    return render(request,
                  f'storefront/themes/{request.store.theme}/index.html',
                  {'store': request.store, 'products': products})


def store_customer_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('/')  # Home or customer dashboard
        return render(request, 'storefront/login.html',
                      {'error': 'Invalid credentials'})
    return render(request, 'storefront/login.html')


def store_customer_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        store = request.store  # from middleware

        user = StoreCustomerUser.objects.create_user(
            email=email,
            name=name,
            store=store,
            password=password
        )
        login(request, user)
        return redirect('/')
    return render(request, 'storefront/register.html')


def store_customer_logout(request):
    logout(request)
    return redirect('/login/')
