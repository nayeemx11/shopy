from django.db import models

class Product_Category(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_length=20, max_digits=20, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} has {self.discount}"

class Product_Inventory(models.Model):
    product_id = models.OneToOneField("Product", on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.quantity)

class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    SKU = models.CharField(max_length=50, null=True, blank=True)
    category_id = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    inventory_id = models.OneToOneField(Product_Inventory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_length=50, max_digits=20, decimal_places=2)
    discount_id = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    discounted_price = models.DecimalField(max_length=20, max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name