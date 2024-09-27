from django.db import models
from user_auth.models import CustomUser, UserPayment
from products.models import Product


class CartItems(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_cart = models.DecimalField(max_digits=100000, decimal_places=2)
    discount_applied = models.CharField(max_length=50, null=True, blank=True)
    added_to_order = models.BooleanField(default=False)  # To track if the item is added to an order
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} (In Cart)"


class OrderItems(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItems, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order of {self.cart_item.quantity} of {self.cart_item.product.name}"


class OrderDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItems, related_name='order_details')
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order Detaisl of{self.order_items} with total {self.total}"
    

class PaymentDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE)

    # JSONField to store details of all products in the cart
    products_info = models.JSONField()  # Store product details as a list of dictionaries

    # Order-specific details
    order_total = models.DecimalField(max_digits=1000, decimal_places=2)  # Total amount for the order
    discount_applied = models.CharField(max_length=50, null=True, blank=True)  # Discount if any

    # Payment-specific details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Failed", "Failed")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.user.username} ({self.status})"

    # Example to get total products count in this payment
    def get_total_products(self):
        return sum(item['quantity'] for item in self.products_info)

