import re
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .models import *
from .forms import RegistrationForm


def validate_password_strength(value):
    """Validates that a password is as least 10 characters long and has at least
    2 digits and 1 Upper case letter.
    """
    min_length = 8

    if len(value) < min_length:
        return f"Password must be at least {min_length} characters long."
    
    if (not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9]){{{0},}}".format(min_length), value)):
        return "Password must contain both letters and digits."

    # check for uppercase letter
    if not any(c.isupper() for c in value):
        return "Password must contain at least 1 uppercase letter."

    return value

# Create your views here.
def home_page(request):
    return render(request, "homepage.html")

def login_page(request):
    
    if request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                messages.success(request, "You have successfully logged in.")
                login(request, user)
                return redirect("Main:home_page")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg.upper()}: {form.error_messages[msg]}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg.upper()}: {form.error_messages[msg]}")
    
    form = AuthenticationForm()
    return render(request,"login.html", context={"form": form})

def register_page(request):
    
    if request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, "You have successfully logged in.")
            login(request, user)
        
            return redirect("Main:home_page")
        else:
            
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            
            if username is None:
                messages.error(request, "Username must not contain any spaces.")
            
            if (password == username):
                 messages.error(request, "Password should not be the same as username.")
            
            validation = validate_password_strength(password)
            
            if (validation != password):
                messages.error(request, validation)
            
            for msg in form.error_messages:
                messages.error(request, f"{msg.upper()}: {form.error_messages[msg]}.")
    
    form = RegistrationForm()
    return render(request, "register.html", context={"form": form})
    
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return HttpResponseRedirect(request.GET.get("next", "/"))