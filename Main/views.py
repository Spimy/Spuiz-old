import json
import random
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate

from .models import *
from .forms import RegistrationForm, LoginForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import reverse

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

def follow_unfollow_success_response(request, user_slug, matching_quizzes):
    
    user = UserProfile.objects.get(slug=user_slug).user
    followings = user.user_profile.following.order_by("username")
    completed_quizzes = CompletedQuiz.objects.filter(
        user__user_profile__slug=user_slug
    ).order_by("-completed_date")
    quiz_urls = {}

    for quiz in matching_quizzes.all():
        quiz_urls[quiz] = quiz.slug
                
    data = {
            "msg": render_to_string(
                "static_html/messages.html",
                {
                    "messages": messages.get_messages(request),
                },
            ),
            "new_page": render_to_string(
                "user_profile.html",
                context={
                    "quizzes": quiz_urls,
                    "viewing_user": user,
                    "followings": followings,
                    "completed_quizzes": completed_quizzes,
                },
                request=request
            )
        }
                
    response = HttpResponse(
        json.dumps(data),
        content_type="application/json",
    )
    response.status_code = 200
    return response


def calculate_rating(quiz):
    upvotes = quiz.upvotes.count()
    downvotes = quiz.downvotes.count()
    fraction = round(upvotes / (upvotes + downvotes), 1)
    
    if fraction < 0.1:
        stars = 0
    elif fraction >= 0.1 and fraction < 0.3:
        stars = 1
    elif fraction >= 0.3 and fraction < 0.5:
        stars = 2
    elif fraction >= 0.5 and fraction < 0.7:
        stars = 3
    elif fraction >= 0.7 and fraction < 0.9:
        stars = 4
    elif fraction >= 0.9:
        stars = 5
        
    remainder = 5 - stars

    return [stars, remainder]

def calculate_percentage_score(score, total_score):
    return round((score / total_score) * 100, 1)

# Create your views here.
def home_page(request):
    newest_quizzes = Quiz.objects.all()[::-1][:10]
    top_quizzes = Quiz.objects.annotate(up_count=Count("upvotes")).order_by("-up_count")[:10]
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
                msg = "You have successfully logged in."
                messages.success(request, msg)
                login(request, user)
                
                response = HttpResponse(msg)
                response.status_code = 200
                return response
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
            msg = "You have successfully registered and logged in."
            
            messages.success(request, msg)
            login(request, user)
        
            response = HttpResponse(msg)
            response.status_code = 200
            return response
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

def user_quiz_slug(request, user_slug, quiz_slug=None, action_slug=None, action=None):
    
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
                        messages.error(request, "You must be logged in to do this.")
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
                
                score = 0
                for key, answer in request.POST.items():
                    if key == "csrfmiddlewaretoken": continue
                    
                    for question in selected_quiz.questions.all():
                        if key.lower() == question.question.lower():
                            
                            answers = question.correct.values("answer")
                            answers = [ans["answer"] for ans in answers]
                            
                            if answer in answers:
                                score += 1
                
                if request.user.is_authenticated:
                    completed = CompletedQuiz.objects.get_or_create(quiz=selected_quiz,
                                                                    user=request.user,
                                                                    score=score)
                    stars, remainder = calculate_rating(selected_quiz)
                    percent = calculate_percentage_score(score, selected_quiz.questions.count())
                    return render(request, "quiz_complete.html",
                                    context={
                                        "completed": completed,
                                        "stars": range(stars),
                                        "remainder": range(remainder),
                                        "percent": percent
                                        }
                                    )
                else:
                    completed = {
                        "score": score,
                        "quiz": selected_quiz
                    }
                    stars, remainder = calculate_rating(selected_quiz)
                    percent = calculate_percentage_score(score, selected_quiz.questions.count())
                    return render(request, "quiz_complete.html",
                                    context={
                                        "completed": completed,
                                        "stars": range(stars),
                                        "remainder": range(remainder),
                                        "percent": percent
                                        }
                                    )

            if action is not None:
                if action == "complete":
                    if request.user.is_authenticated:
                        try:
                            completed = CompletedQuiz.objects.get(quiz=selected_quiz, user=request.user)
                            stars, remainder = calculate_rating(selected_quiz)
                            percent = calculate_percentage_score(completed.score, selected_quiz.questions.count())
                            
                            return render(request, "quiz_complete.html",
                                          context={
                                              "completed": completed,
                                              "stars": range(stars),
                                              "remainder": range(remainder),
                                              "percent": percent
                                              }
                                          )
                        except CompletedQuiz.DoesNotExist:
                            return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)
                    else:
                        return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)
                else:
                    raise Http404("Unknown action")
                    
            if request.user.is_authenticated:
                try:
                    completed = CompletedQuiz.objects.get(quiz=selected_quiz, user=request.user)
                    return redirect("Main:user_quiz_completed_slug",
                                    user_slug=user_slug,
                                    quiz_slug=quiz_slug,
                                    action="complete")
                except CompletedQuiz.DoesNotExist:
                    return render(request, "quiz_page.html", context={"quiz": quiz})
        
            return render(request, "quiz_page.html", context={"quiz": quiz})
        
        elif action_slug is not None:
            
            if request.method == "POST":
                if request.user.is_authenticated:
                    
                    user = UserProfile.objects.get(slug=user_slug).user
                    
                    if action_slug == "follow":
                        
                        if request.user == user:
                            messages.error(request, "You cannot follow yourself.")
                            return error_msg_response(request)
                        
                        if user not in request.user.user_profile.following.all():
                            request.user.user_profile.following.add(user)
                            messages.success(request, f"You are now following {user.username}.")
                            return follow_unfollow_success_response(request, user_slug, matching_quizzes)
                        else:
                            messages.error(request, f"You are already following {user.username}")
                            return error_msg_response(request)
                            
                    elif action_slug == "unfollow":
                        
                        if request.user == user:
                            messages.error(request, "You cannot unfollow yourself.")
                            return error_msg_response(request)
                        
                        if user in request.user.user_profile.following.all():
                            request.user.user_profile.following.remove(user)
                            messages.success(request, f"You are no longer following {user.username}.")
                            return follow_unfollow_success_response(request, user_slug, matching_quizzes)
                        else:
                            messages.error(request, f"You are not following {user.username}")
                            return error_msg_response(request)
                        
                    else:
                        raise Http404("Unknown action")
                else:
                    messages.error(request, "You must be logged in to do this")
                    return error_msg_response(request)
            else:
                return redirect("Main:user_slug", user_slug=user_slug)
        
        else:
            
            user = UserProfile.objects.get(slug=user_slug).user
            followings = user.user_profile.following.order_by("username")
            completed_quizzes = CompletedQuiz.objects.filter(
                user__user_profile__slug=user_slug
            ).order_by("-completed_date")
            quiz_urls = {}

            for quiz in matching_quizzes.all():
                quiz_urls[quiz] = quiz.slug
            return render(request, "user_profile.html", context={"quizzes": quiz_urls,
                                                                 "viewing_user": user,
                                                                 "followings": followings,
                                                                 "completed_quizzes": completed_quizzes})

    raise Http404("User not found")

def handler404(request, exception):
    response = render(request, "errors/404.html", context={"exception": exception})
    return response