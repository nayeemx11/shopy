from django.shortcuts import render, redirect
from .models import *
from .forms import ProductCategoryForm, DiscountForm, ProductForm, ProductInventoryForm


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        context = {"message": f"Welcome back, {username}!"}
    else:
        context = {"message": "Please sign up or log in to access your account."}

    return render(request, "index.html", context)


def product_home(request):
    # Get all products that are not deleted (assuming deleted_at is used for soft deletion)
    products = Product.objects.filter(deleted_at__isnull=True).select_related(
        "category_id",
        "inventory_id",
        "discount_id",
    )

    context = {"products": products}
    return render(request, "products/product_home.html", context)


def category_create_view(request):
    category_form = ProductCategoryForm(request.POST)
    if category_form.is_valid():
        category_form.save()
        return redirect("addnewproduct")
    else:
        category_form = ProductCategoryForm()

    context = {"category_form": category_form}
    return render(request, "products/addnewproduct.html", context)


def discount_create_view(request):
    discount_form = DiscountForm(request.POST)
    if discount_form.is_valid():
        discount_form.save()
        return redirect("addnewproduct")
    else:
        discount_form = DiscountForm()

    context = {"discount_form": discount_form}
    return render(request, "products/addnewproduct.html", context)


def inventory_create_view(request):
    inventory_form = ProductInventoryForm(request.POST)
    if inventory_form.is_valid():
        inventory_form.save()
        return redirect("addnewproduct")
    else:
        inventory_form = ProductInventoryForm()

    context = {"inventory_form": inventory_form}
    return render(request, "products/addnewproduct.html", context)

def connectAllthingsUp():
    products = Product.objects.filter(deleted_at__isnull=True).select_related(
        "category_id",
        "inventory_id",
        "discount_id",
    )

    for product in products:

        if product.inventory_id:
            product.inventory_id.name = product.name
            product.save()

        if product.discount_id and product.discount_id.active:
            product.discounted_price = product.price - (
                product.price * product.discount_id.discount / 100
            )
            product.save()
        else:
            product.discounted_price = product.price

def product_create_view(request):
    product_form = ProductForm(request.POST)
    if product_form.is_valid():
        product_form.save()
        connectAllthingsUp()
        return redirect("addnewproduct")
    else:
        product_form = ProductForm()

    context = {"product_form": product_form}
    return render(request, "products/addnewproduct.html", context)




def create_view(request):
    category_form = ProductCategoryForm()
    discount_form = DiscountForm()
    inventory_form = ProductInventoryForm()
    product_form = ProductForm()

    if request.method == "POST":
        if "category_submit" in request.POST:
            category_create_view(request)
        elif "discount_submit" in request.POST:
            discount_create_view(request)
        elif "inventory_submit" in request.POST:
            inventory_create_view(request)
        elif "product_submit" in request.POST:
            product_create_view(request)

    context = {
        "category_form": category_form,
        "discount_form": discount_form,
        "product_form": product_form,
        "inventory_form": inventory_form,
    }

    return render(request, "products/addnewproduct.html", context)
