from django import forms
from .models import CartItems, OrderItems, PaymentDetails

class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ["status"]


# 1st order items, what item is ordering, how many, total cost
# 2nd confirm payment
# 3rd order details payment recipet
