from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(CartItems)
admin.site.register(OrderItems)
admin.site.register(OrderDetails)
admin.site.register(PaymentDetails)