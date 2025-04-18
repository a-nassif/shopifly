from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

from store.models import Store, Product
from storefront.models import StoreCustomerUser


# Create your models here.

class StoreOwnerManager(BaseUserManager):
    def create_user(self, email, store, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, store=store, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class StoreOwnerUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    store = models.OneToOneField('store.Store', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['store']

    objects = StoreOwnerManager()

    def __str__(self):
        return f"Owner: {self.email} ({self.store.subdomain})"


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(StoreCustomerUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"

    def calculate_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def get_total_price(self):
        return self.quantity * self.unit_price