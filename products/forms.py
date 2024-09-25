from django import forms
from .models import Product_Category, Discount, Product, Product_Inventory


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Product_Category
        fields = ['name', 'desc']
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'desc', 'discount', 'active']
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'desc', 'SKU', 'category_id', 'inventory_id', 'price', 'discount_id']
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ProductInventoryForm(forms.ModelForm):
    class Meta:
        model = Product_Inventory
        fields = ['quantity']