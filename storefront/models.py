from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

from store.models import Store, Product


# Create your models here.

class StoreCustomerUserManager(BaseUserManager):
    def create_user(self, store, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(store=store, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class StoreCustomerUser(AbstractBaseUser):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    email = models.EmailField(unique=False)  # Allow same email in different stores
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = StoreCustomerUserManager()

    class Meta:
        unique_together = ('store', 'email')  # Unique per store

    def __str__(self):
        return f"{self.email} ({self.store.subdomain})"


class Cart(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.select_related('product'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"