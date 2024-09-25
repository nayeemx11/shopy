from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItems, OrderItems, OrderDetails, PaymentDetails
from products.models import Product
from django.db.models import Sum


@login_required
def buy_now(request, product_id):
    """Add product to cart for immediate purchase (buy now functionality)."""
    product = get_object_or_404(Product, id=product_id)

    # Add the product to the cart (or increment quantity if already exists)
    cart_item, created = CartItems.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1, "price_cart": product.price},
    )

    if not created:
        # Update price if the item already exists and quantity is increased
        cart_item.price_cart = cart_item.product.price * cart_item.quantity
        cart_item.save()

    print(cart_item)

    # Redirect to the buy now view with the single cart item
    return redirect("buynow_view", cart_item_id=cart_item.id)


@login_required
def buynow_view(request, cart_item_id):
    """Directly purchase a single product (Buy Now) from the cart."""
    cart_item = get_object_or_404(CartItems, id=cart_item_id, user=request.user)

    # Create a new order
    order = OrderItems.objects.create(user=request.user)

    # Link the single cart item to the order
    order.cart_items.add(cart_item)

    # Mark the cart item as ordered
    cart_item.added_to_order = True
    cart_item.save()

    # Calculate the total price (for a single item, it’s the product price * quantity)
    total_price = cart_item.product.price * cart_item.quantity

    # Create an OrderDetails instance
    OrderDetails.objects.create(order_items=order, total=total_price)

    return redirect("order_summary", order_id=order.id)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItems.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1, "price_cart": product.price},
    )

    # Increase quantity if already exists in cart
    if not created:
        cart_item.quantity += 1
        cart_item.price_cart = cart_item.product.price * cart_item.quantity
        cart_item.save()

    print(cart_item)

    return redirect("product_home")


@login_required
def cart_view(request):
    """View items in the cart."""
    cart_items = CartItems.objects.filter(user=request.user)
    total_price = sum(cart.price_cart for cart in cart_items)
    return render(
        request,
        "order/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItems, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart_view")


@login_required
def place_order(request):
    """Place an order with items from the cart."""
    cart_items = CartItems.objects.filter(user=request.user)
    print(cart_items)

    if not cart_items.exists():
        return redirect("cart_view")  # No items in the cart

    # Create a new order
    order = OrderItems.objects.create(user=request.user)
    order.cart_items.set(cart_items)  # Link cart items to the order

    # Mark cart items as added to order
    cart_items.update(added_to_order=True)

    # Calculate total price for the order
    total_price = sum(cart.price_cart for cart in cart_items)

    # Create an OrderDetails instance
    OrderDetails.objects.create(order_items=order, total=total_price)

    return redirect("order_summary", order_id=order.id)


@login_required
def order_summary(request, order_id):
    """View order summary after placing an order."""
    order = get_object_or_404(OrderItems, id=order_id, user=request.user)
    order_details = get_object_or_404(OrderDetails, order_items=order)
    return render(
        request,
        "order/order_summary.html",
        {"order": order, "order_details": order_details},
    )
