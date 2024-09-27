from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItems, OrderItems, OrderDetails, PaymentDetails
from products.models import Product
from user_auth.models import UserPayment
from django.db.models import Sum

from .forms import PaymentDetailsForm


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
        cart_item.quantity += 1
        cart_item.price_cart = cart_item.product.price * cart_item.quantity
        cart_item.save()

    print(cart_item)

    # Redirect to the buy now view with the single cart item
    return redirect("buynow_view", cart_item_id=cart_item.id)


@login_required
def buynow_view(request, cart_item_id):
    """Directly purchase a single product (Buy Now) from the cart."""
    cart_item = get_object_or_404(CartItems, id=cart_item_id, user=request.user)

    # Create a new order item for the cart item
    order_item = OrderItems.objects.create(user=request.user, cart_item=cart_item)

    # Create an OrderDetails instance
    order_details = OrderDetails.objects.create(
        user=request.user, total=cart_item.price_cart
    )

    # Add the newly created order item to the order details
    order_details.order_items.add(order_item)

    return redirect("order_summary", order_details_id=order_details.id)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)

    # Create or update cart item
    cart_item, created = CartItems.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1, "price_cart": product.price},
    )

    if not created:
        # If the item already exists, increase quantity
        cart_item.quantity += 1  # Adjust quantity as needed
        cart_item.price_cart = cart_item.product.price * cart_item.quantity
        cart_item.save()

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

    if not cart_items.exists():
        messages.error(request, "No items in the cart.")
        return redirect("cart_view")  # No items in the cart

    total_price = 0
    order_items = []

    # Loop through each cart item and create an order for each
    for cart_item in cart_items:
        # Create a new order for each cart item
        order = OrderItems.objects.create(user=request.user, cart_item=cart_item)

        # Mark cart item as added to order
        cart_item.added_to_order = True
        cart_item.save()

        # Add to the total price
        total_price += cart_item.price_cart

        order_items.append(order)  # Collect all created orders

    # Create an OrderDetails instance after creating all orders
    order_details = OrderDetails.objects.create(total=total_price, user=request.user)

    # Now add all the order items to the OrderDetails instance
    order_details.order_items.set(
        order_items
    )  # Add the created order items to the order_details

    # After all orders are created, you might want to redirect to the order summary
    return redirect("order_summary", order_details_id=order_details.id)


@login_required
def order_summary(request, order_details_id):
    """View order summary and apply discounts to multiple cart items in an order."""

    # order_details = OrderDetails.objects.get_or_create(user=request.user, id=order_details_id)
    order_details = get_object_or_404(
        OrderDetails, user=request.user, id=order_details_id
    )

    if request.method == "POST":
        discount_str = request.POST.get("discount_str", "")

        # Iterate through the multiple OrderItems
        for (
            order_item
        ) in order_details.order_items.all():  # Accessing all related order items
            cart_item = order_item.cart_item  # Access the related cart item

            # Check if the discount is valid and apply it
            if (
                cart_item.product.discount_id
                and cart_item.product.discount_id.name == discount_str
                and cart_item.product.discount_id.active
            ):
                cart_item.price_cart = (
                    cart_item.product.discounted_price * cart_item.quantity
                )
                cart_item.save()

        # Update the total in the single order_details instance
        total_price = sum(
            [
                order_item.cart_item.price_cart
                for order_item in order_details.order_items.all()
            ]
        )
        order_details.total = total_price
        order_details.save()

        return redirect("order_summary", order_details_id=order_details.id)

    order_items = order_details.order_items.all()

    # Pass all required context to the template
    return render(
        request,
        "order/order_summary.html",
        {
            "order_items": order_items,
            "order_details": order_details,  # Correcting variable name here
        },
    )


@login_required
def confirm_order(request, order_details_id):
    """View order summary and confirm the order."""
    # order = get_object_or_404(OrderItems, id=order_id, user=request.user)
    order_details = get_object_or_404(OrderDetails, id=order_details_id)
    payment_account = get_object_or_404(UserPayment, user=request.user)

    # Prepare product details to store in the JSONField
    product_info = []
    cart_items = CartItems.objects.filter(user=request.user)

    for item in cart_items:
        product_info.append(
            {
                "product_name": item.product.name,
                "product_price": str(
                    item.price_cart
                ),  # Convert Decimal to string for JSON
                "product_quantity": item.quantity,
            }
        )

    # Create or update PaymentDetails instance
    payment_detail = PaymentDetails.objects.create(
        user=request.user,
        payment=payment_account,
        products_info=product_info,
        order_total=order_details.total,
        amount=order_details.total,
        status="Pending",
    )

    if request.method == "POST":
        print(request.method)
        payment_form = PaymentDetailsForm(request.POST, instance=payment_detail)
        if payment_form.is_valid():
            print("form valid")
            payment_detail = payment_form.save(
                commit=False
            )  # Save payment details but don't commit yet

            # Check inventory and reduce product quantity
            all_items_available = True
            for item in cart_items:
                print(item)
                inventory = item.product.inventory_id
                if inventory.quantity < item.quantity:
                    all_items_available = False
                    messages.error(
                        request, f"Not enough stock for {item.product.name}."
                    )
                    # print("break")
                    break

            if all_items_available:
                # Deduct inventory quantities
                for item in cart_items:
                    inventory = item.product.inventory_id
                    inventory.quantity -= item.quantity
                    inventory.save()
                    print("invetonry saved")

                # print(request)
                # print(payment_form)

                # Update payment status based on the form
                if payment_detail.status == "Paid":
                    print("Payment status set to 'Paid'")
                    payment_detail.status = "Paid"
                    payment_detail.save()

                    # Clear the cart and delete the orders
                    for item in cart_items:
                        item.delete()
                    OrderItems.objects.filter(user=request.user).delete()
                    OrderDetails.objects.filter(user=request.user).delete()

                return redirect("payment_history")

    else:
        payment_form = PaymentDetailsForm(instance=payment_detail)

    return render(
        request,
        "order/confirm_order.html",
        {
            "order_details": order_details,
            "payment_form": payment_form,
        },
    )


@login_required
def payment_history(request):
    """View payment history of the logged-in user."""
    paymenthistory = PaymentDetails.objects.filter(user=request.user)

    return render(
        request, "order/payment_history.html", {"paymenthistory": paymenthistory}
    )


@login_required
def payment_history_super(request):
    """View payment history of the logged-in user."""
    
    # Check if the user is a superuser
    if request.user.is_superuser:
        # If the user is a superuser, fetch all payment details
        paymenthistory = PaymentDetails.objects.all()
    else:
        # Otherwise, fetch only the payment details for the logged-in user
        paymenthistory = PaymentDetails.objects.filter(user=request.user)

    return render(
        request, "order/payment_history.html", {"paymenthistory": paymenthistory}
    )


# history
# payment
# login button signup button
