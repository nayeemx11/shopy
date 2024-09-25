from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm
from .models import CustomUser

def alreadyLoggedIn(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("index") # change it 

def signup(request):
    
    alreadyLoggedIn(request)
    
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            username = signup_form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            auth_login(request, user)  # Automatically log in the user after signup
            return redirect("index")  # Redirect to the index or login page after registration
    else:
        signup_form = CustomUserCreationForm()

    return render(request, "user_auth/signup.html", {"signup_form": signup_form})


def login_view(request):
    
    alreadyLoggedIn(request)
    
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log in the user
                messages.success(request, f"Welcome back, {username}!")
                return redirect("login")  # Redirect to the post list or any other page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        login_form = AuthenticationForm()

    return render(request, "user_auth/login.html", {"login_form": login_form})


@require_http_methods(["GET", "POST"])
def logout(request):
    """
    Handles user logout.

    Logs out the currently authenticated user and redirects to the index page.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: A redirect to the index page.
    """
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("index")
