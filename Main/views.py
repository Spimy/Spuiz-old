import re
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .models import *
from .forms import RegistrationForm


def validate_password_strength(value):
    
    min_length = 8

    if len(value) < min_length:
        return f"Password must be at least {min_length} characters long."
    
    if (not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9]){{{0},}}".format(min_length), value)):
        return "Password must contain both letters and digits."

    # check for uppercase letter
    if not any(c.isupper() for c in value):
        return "Password must contain at least 1 uppercase letter."

    return value

def user_slug(request, user_slug):
    users = [u.slug for u in UserProfile.objects.all()]
    if user_slug in users:

        matching_quizzes = Quiz.objects.filter(user_profile__slug=user_slug)
        quiz_urls = {}

        for quiz in matching_quizzes.all():
            quiz_urls[quiz] = quiz.slug

        return render(request, "user_profile.html", context={"quizzes": quiz_urls})

def quiz_slug(request, user_slug, quiz_slug):
    users = [u.slug for u in UserProfile.objects.all()]
    if user_slug in users:

        matching_quizzes = Quiz.objects.filter(user_profile__slug=user_slug)
        selected_quiz = matching_quizzes.filter(slug=quiz_slug)

        return render(request, "quiz_page.html", context={"quiz": selected_quiz})

# Create your views here.
def home_page(request):
    quizzes = Quiz.objects.all()[::-1]
    return render(request, "homepage.html", context={"quizzes": quizzes})

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