from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from products.models import Product

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.username

class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50, null=True, blank=True)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paymentType = models.CharField(max_length=20)
    provider = models.CharField(max_length=20, null=True, blank=True)
    account_no = models.IntegerField()
    expiry = models.DateField(null=True, blank=True)