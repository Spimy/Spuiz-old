import json
import random
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate

from .models import *
from .forms import RegistrationForm, LoginForm
from django.db.models import Count


def error_msg_response(request):
    data = {
                    "msg": render_to_string(
                        "static_html/messages.html",
                        {
                            "messages": messages.get_messages(request),
                        },
                    ),
                }
                
    response = HttpResponse(
        json.dumps(data),
        content_type="application/json",
    )
    response.status_code = 218
    return response


# Create your views here.
def home_page(request):
    newest_quizzes = Quiz.objects.all()[::-1]
    top_quizzes = Quiz.objects.annotate(up_count=Count("upvotes")).order_by("-up_count")
    return render(request, "homepage.html", context={"newest_quizzes": newest_quizzes, 
                                                     "top_quizzes": top_quizzes})

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
                
                response = {
                            "msg": render_to_string(
                                "static_html/messages.html",
                                {
                                    "messages": messages.get_messages(request),
                                },
                            ),
                        }
                        
            res =  HttpResponse(
                json.dumps(response),
                content_type="application/json",
            )
            res.status_code = 218
        
            return res
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg.upper()}: {form.error_messages[msg]}")
                
            return error_msg_response(request)
    
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

            errors = json.loads(form.errors.as_json())

            for msg in errors:
                
                error_msg = errors[msg][0]["message"]
                
                if errors[msg][0]["code"] != "":
                    error_msg = errors[msg][0]["code"].upper() + ": " + error_msg
                    
                messages.error(request, error_msg)
                
            return error_msg_response(request)
    
    form = RegistrationForm()
    return render(request, "register.html", context={"form": form})
    
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return HttpResponseRedirect(request.GET.get("next", "/"))

def user_quiz_slug(request, user_slug, quiz_slug=None):
    
    users = [u.slug for u in UserProfile.objects.all()]
    if user_slug in users:

        matching_quizzes = Quiz.objects.filter(author__user_profile__slug=user_slug)
        
        if quiz_slug is not None:
            
            try:
                selected_quiz = matching_quizzes.get(slug=quiz_slug)
            except Quiz.DoesNotExist:
                raise Http404("Quiz not found")
            
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
            
            if request.method == "POST":

                if "vote" in list(request.POST.keys()):
                    if not request.user.is_authenticated:
                        messages.error(request, "You must be logged in to do this!")
                        return error_msg_response(request)
                    
                    if request.POST["vote"] == "upvote":
                        
                        if request.user in selected_quiz.downvotes.all():
                            selected_quiz.downvotes.remove(request.user)
                            
                        if request.user in selected_quiz.upvotes.all():
                            selected_quiz.upvotes.remove(request.user)
                        else:
                            selected_quiz.upvotes.add(request.user)
                        
                    else:
                        
                        if request.user in selected_quiz.upvotes.all():
                            selected_quiz.upvotes.remove(request.user)
                            
                        if request.user in selected_quiz.downvotes.all():
                            selected_quiz.downvotes.remove(request.user)
                        else:
                            selected_quiz.downvotes.add(request.user)
                        
                    response = {
                            "updownvotebtns": render_to_string("quiz_page.html", 
                                                            context={"quiz": quiz}, 
                                                            request=request),
                        }
                    
                    return HttpResponse(
                            json.dumps(response),
                            content_type="application/json",
                    )
                
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

            return render(request, "quiz_page.html", context={"quiz": quiz})
        else :
            quiz_urls = {}

            for quiz in matching_quizzes.all():
                quiz_urls[quiz] = quiz.slug

            return render(request, "user_profile.html", context={"quizzes": quiz_urls})

    raise Http404("User not found")

def handler404(request, exception):
    response = render(request, "errors/404.html", context={"exception": exception})
    return response