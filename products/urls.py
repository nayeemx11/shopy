from django.urls import path, include
from . import views
# from . import views_stuff

urlpatterns = [
    path('', views.index, name="index"),
    path('product_home', views.product_home, name="product_home"),
    path('addnewproduct', views.create_view, name='addnewproduct'),
    # path('product_form/', views_stuff.create_product, name='product_form'),
]
