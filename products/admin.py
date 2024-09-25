from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Discount)
admin.site.register(models.Product_Inventory)
admin.site.register(models.Product_Category)