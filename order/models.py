from django.db import models
from user_auth.models import CustomUser, UserPayment
from products.models import Product


class CartItems(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_cart = models.DecimalField(max_digits=1000, decimal_places=2)
    added_to_order = models.BooleanField(default=False)  # To track if the item is added to an order
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} (In Cart)"


class OrderItems(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItems)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        cart_summary = ", ".join(
            [
                f"{item.quantity} of {item.product.name}"
                for item in self.cart_items.all()
            ]
        )
        return f"Order of {cart_summary}"


class OrderDetails(models.Model):
    order_items = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

class PaymentDetails(models.Model):
    payment = models.OneToOneField(UserPayment, on_delete=models.CASCADE)
    order_details = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Failed", "Failed")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order_details.id}: {self.status}"
