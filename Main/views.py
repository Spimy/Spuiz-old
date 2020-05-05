import json
import random
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .models import *
from .forms import RegistrationForm, LoginForm
from django.http.response import HttpResponse


# Create your views here.
def home_page(request):
    quizzes = Quiz.objects.all()[::-1]
    return render(request, "homepage.html", context={"quizzes": quizzes})

def login_page(request):
    
    if request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
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
    
    form = LoginForm()
    return render(request,"login.html", context={"form": form})

def register_page(request):
    
    if request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, "You have successfully registered and logged in.")
            login(request, user)
        
            return redirect("Main:home_page")
        else:
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg.upper()}: {form.error_messages[msg]}.")
            errors = json.loads(form.errors.as_json())
            print(errors)
            for msg in errors:
                
                error_msg = errors[msg][0]['message']
                
                if errors[msg][0]['code'] != "":
                    error_msg = errors[msg][0]['code'].upper() + ": " + error_msg
                    
                messages.error(request, error_msg)
    
    form = RegistrationForm()
    return render(request, "register.html", context={"form": form})
    
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return HttpResponseRedirect(request.GET.get("next", "/"))

def user_slug(request, user_slug):
    
    users = [u.slug for u in UserProfile.objects.all()]
    if user_slug in users:

        matching_quizzes = Quiz.objects.filter(author__user_profile__slug=user_slug)
        quiz_urls = {}

        for quiz in matching_quizzes.all():
            quiz_urls[quiz] = quiz.slug

        return render(request, "user_profile.html", context={"quizzes": quiz_urls})

def quiz_slug(request, user_slug, quiz_slug):
    
    users = [u.slug for u in UserProfile.objects.all()]
    if user_slug in users:

        matching_quizzes = Quiz.objects.filter(author__user_profile__slug=user_slug)
        selected_quiz = matching_quizzes.filter(slug=quiz_slug)[0]
        
        if request.method == "POST":
            correct = 0
            for key, answer in request.POST.items():
                if key == "csrfmiddlewaretoken": continue
                
                for question in selected_quiz.questions.all():
                    if key.lower() == question.question.lower():
                        
                        answers = question.correct.values("answer")
                        answers = [ans["answer"] for ans in answers]
                        
                        if answer in answers:
                            correct += 1
                            
            return HttpResponse(correct)
        
        flatten = lambda l: [item for sublist in l for item in sublist]
        questions = {}
        
        for question in selected_quiz.questions.all():
            answers = []
            answers.append([question.correct.first()])
            answers.append(question.wrong.all())
            
            answers = flatten(answers)
            random.shuffle(answers)
            questions[question] = answers
            
        quiz = {
            "questions": questions,
            "quiz_info": selected_quiz
            }

        return render(request, "quiz_page.html", context={"quiz": quiz})
