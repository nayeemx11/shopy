from django.urls import path
from . import views

urlpatterns = [
    path("buy_now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("buynow_view/<int:cart_item_id>/", views.buynow_view, name="buynow_view"),
    path("order_summary/<int:order_details_id>/", views.order_summary, name="order_summary"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart_view", views.cart_view, name="cart_view"),
    path("remove_from_cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("place_order/", views.place_order, name="place_order"),
    path("confirm_order/<int:order_details_id>/", views.confirm_order, name="confirm_order"),
    path("payment_history/", views.payment_history, name="payment_history"),
    path("payment_history_super/", views.payment_history_super, name="payment_history_super"),
]
