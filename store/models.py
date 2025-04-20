import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# store/models/store.py
from django.db import models

from store_admin.constants import CURRENCY_OPTIONS


class Store(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.SlugField(max_length=100, unique=True)
    custom_domain = models.CharField(max_length=255, unique=True, null=True,
                                     blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional extras
    logo = models.ImageField(upload_to='store_logos', null=True, blank=True)
    brand_color = models.CharField(max_length=7, default='#000000')  # HEX color
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True,
                              blank=True)
    # theme = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=10, default='IQD',
                                choices=CURRENCY_OPTIONS)

    def __str__(self):
        return f"{self.name} ({self.subdomain})"

    def full_domain(self, request):
        """Return a custom domain if available, fallback to subdomain."""
        current_host = request.get_host()
        if self.custom_domain:
            return self.custom_domain
        # elif current_host == 'localhost:8000':
        return f"{request.scheme}://{self.subdomain}.{request.get_host()}"


class Theme(models.Model):
    name = models.CharField(max_length=255)
    template_path = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to='theme_previews', null=True,
                                      blank=True)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def for_store(self, store):
        return self.filter(store=store)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()

    objects = ProductManager()
