from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

# storefront/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from store.models import Product
from .forms import StoreCustomerRegisterForm
from .models import StoreCustomerUser


def store_home(request):
    products = request.store.product_set.all()
    return render(request,
                  f'storefront/themes/{request.store.theme.template_path}/index.html',
                  {'store': request.store, 'products': products})


def store_customer_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('store_home'))
    template_extend_path = f'storefront/themes/{request.store.theme.template_path}/base.html'
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(
                reverse('home_dispatcher'))  # Home or customer dashboard
        return render(request, 'storefront/login.html',
                      {'error': 'Invalid credentials',
                       'extend_path': template_extend_path})

    return render(request, 'storefront/login.html',
                  {'extend_path': template_extend_path})


def store_customer_register(request):
    template_extend_path = f'storefront/themes/{request.store.theme.template_path}/base.html'
    if request.method == 'POST':
        form = StoreCustomerRegisterForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.set_password(form.cleaned_data['password'])
            customer.store = request.store  # Inject current store from middleware
            customer.save()
            # Auto login? Or redirect to login
            user = authenticate(request, username=customer.email,
                                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('home_dispatcher')
        else:
            return render(request, 'storefront/register.html',
                          {'form': form, 'extend_path': template_extend_path})
    else:
        form = StoreCustomerRegisterForm()

    return render(request, 'storefront/register.html',
                  {'form': form, 'extend_path': template_extend_path})


def store_customer_logout(request):
    logout(request)
    return redirect(reverse('home_dispatcher'))


def product_detail(request, pk):
    template_extend_path = f'storefront/themes/{request.store.theme.template_path}/base.html'
    product = get_object_or_404(Product, pk=pk, store=request.store)
    return render(request, f'storefront/themes/theme_1/product_details.html',
                  {'product': product, 'extend_path': template_extend_path})


def add_to_cart(request, pk):
    quantity = int(request.POST.get("quantity", 1))
    product = get_object_or_404(Product, pk=pk, store=request.store)

    # pseudo-code:
    # cart = get_or_create_cart(request)
    # cart.add(product, quantity)

    return redirect('product_detail', pk=pk)