from django import forms
from .models import CartItems, OrderItems, PaymentDetails






class CartItemsFrom(forms.ModelForm):
    class Meta:
        model = CartItems
        fields = ["quantity"]


class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ["amount", "status"]


# 1st order items, what item is ordering, how many, total cost
# 2nd confirm payment
# 3rd order details payment recipet
