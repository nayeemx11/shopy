from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("user_auth.urls")),
    path("", include("products.urls")),
    path("order/", include("order.urls")),
]
