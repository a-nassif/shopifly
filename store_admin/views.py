from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from store.forms import ProductForm
from store.models import Store
from .forms import StoreSettingsForm, StoreOwnerRegistrationForm
from .models import StoreOwnerUser


def store_owner_login(request):
    if request.user.is_authenticated and hasattr(request.user, 'store'):
        return redirect(
            reverse('store_admin:store_dashboard'))
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(
                reverse('store_admin:store_dashboard'))  # Change as needed
        return render(request, 'store_admin/login.html',
                      {'error': 'Invalid credentials'})
    return render(request, 'store_admin/login.html')


def store_owner_register(request):
    if request.user.is_authenticated and hasattr(request.user, 'store'):
        return redirect(
            reverse('store_admin:store_dashboard'))
    if request.method == 'POST':
        form = StoreOwnerRegistrationForm(request.POST)
        if form.is_valid():
            store = Store.objects.create(
                name=form.cleaned_data['store_name'],
                subdomain=form.cleaned_data['subdomain']
            )
            user = StoreOwnerUser.objects.create_user(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                password=form.cleaned_data['password'],
                store=store
            )
            user = authenticate(request, username=user.email, password=form.cleaned_data['password'])
            login(request, user)
            return redirect(
                reverse('store_admin:store_dashboard'))  # Or wherever you want
    else:
        form = StoreOwnerRegistrationForm()

    return render(request, 'store_admin/register.html', {'form': form})


def store_owner_logout(request):
    logout(request)
    return redirect('marketing_landing')


@login_required
# @store_owner_required
def store_settings_view(request):
    store = request.user.store

    if request.method == 'POST':
        form = StoreSettingsForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings Updated Successfully.")
            return redirect(reverse(
                'store_admin:store_settings'))  # or show a success message
    else:
        form = StoreSettingsForm(instance=store)

    store_domain = store.full_domain(request)

    return render(request, 'store_admin/store_settings.html',
                  {'form': form, 'store_domain': store_domain})


@login_required
# @store_owner_required
def store_dashboard_view(request):
    return render(request, 'store_admin/dashboard.html')


def check_store_domain(request):
    subdomain = request.GET.get('subdomain')
    custom_domain = request.GET.get('custom_domain')

    response = {}

    if subdomain:
        exists = Store.objects.filter(subdomain=subdomain).exclude(
            id=request.store.id).exists()
        response['subdomain_taken'] = exists

    if custom_domain:
        exists = Store.objects.filter(custom_domain=custom_domain).exclude(
            id=request.store.id).exists()
        response['custom_domain_taken'] = exists

    return JsonResponse(response)

@login_required
def store_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = request.user.store
            product.save()
            return redirect('store_admin:store_products')
    else:
        form = ProductForm()
    products = request.user.store.product_set.all()

    return render(request, 'store_admin/products.html',
                  {'products': products, 'form': form})
