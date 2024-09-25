from django.urls import path, include
from . import views

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout, name="logout"),
]