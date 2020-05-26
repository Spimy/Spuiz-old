import json
import random
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.db.models import Count
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from .models import *
from .forms import *
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
    
    if (upvotes + downvotes) == 0:
        return [0, 5]
    
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
    newest_quizzes = Quiz.objects.all().order_by("-pk")[:10]
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

def settings_page(request):
    
    if not request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        
        user_profile = request.user.user_profile
        
        if "bio" in list(request.POST.keys()):
            
            user_profile.bio = request.POST["bio"]
            user_profile.save()
            
            messages.success(request, "Your biography has been successfully updated.")
        
        elif "avatar" in list(request.FILES.keys()):
            
            user_profile.avatar = request.FILES["avatar"]
            user_profile.save()
            
            messages.success(request, "Your avatar has been successfully updated.")
        
        elif "banner" in list(request.FILES.keys()):
            
            user_profile.banner = request.FILES["banner"]
            user_profile.save()
            
            messages.success(request, "Your banner has been successfully updated.")
                    
        else:
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Your account information has been successfully updated.")
            else:
                # messages.error(request, "An error has occurred while trying to save your account information.")
                errors = json.loads(form.errors.as_json())

                for msg in errors:
                    
                    error_msg = errors[msg][0]["message"]
                    
                    if errors[msg][0]["code"] != "":
                        error_msg = errors[msg][0]["code"].upper() + ": " + error_msg
                        
                    messages.error(request, error_msg)
                 
                data = {
                        "msg": render_to_string(
                            "static_html/messages.html",
                            {
                                "messages": messages.get_messages(request),
                            },
                        )
                    }
                            
                response = HttpResponse(
                    json.dumps(data),
                    content_type="application/json",
                )
                response.status_code = 218
                return response
                        
        data = {
                "msg": render_to_string(
                    "static_html/messages.html",
                    {
                        "messages": messages.get_messages(request),
                    },
                ),
                "settings": render_to_string(
                    "settings.html",
                    request=request
                )
            }
                    
        response = HttpResponse(
            json.dumps(data),
            content_type="application/json",
        )
        response.status_code = 200
        return response
                    
    form = UserEditForm(instance=request.user)
    return render(request, "settings.html", context={"form": form})

def user_quiz_slug(request, user_slug, quiz_slug=None, action_slug=None):
    
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

                    if request.POST["from_complete"] != "true":
                        response = {
                                "updownvotebtns": render_to_string("quiz_page.html", 
                                                                context={"quiz": quiz}, 
                                                                request=request),
                            }
                    else:
                        completed = CompletedQuiz.objects.get(quiz=selected_quiz, user=request.user)
                        stars, remainder = calculate_rating(selected_quiz)
                        percent = calculate_percentage_score(completed.score, selected_quiz.questions.count())
                        response = {
                            "updownvotebtns": render_to_string("quiz_complete.html",
                                                               context={
                                                                   "completed": completed,
                                                                    "stars": range(stars),
                                                                    "remainder": range(remainder),
                                                                    "percent": percent
                                                               },
                                                               request=request)
                        }
                        
                    return HttpResponse(
                            json.dumps(response),
                            content_type="application/json",
                    )
                
                score = 0
                for key, answer in request.POST.items():
                    if key == "csrfmiddlewaretoken": continue
                    
                    for question in selected_quiz.questions.all():
                        if int(key) == question.pk:
                            
                            answers = question.correct.values("answer")
                            answers = [ans["answer"].lower() for ans in answers]
                            
                            if answer.lower() in answers:
                                score += 1
                
                if request.user.is_authenticated:
                    CompletedQuiz.objects.get_or_create(quiz=selected_quiz,
                                                        user=request.user,
                                                        score=score)
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
            ).order_by("-completed_date")[:4]
            quiz_urls = {}

            for quiz in matching_quizzes.all():
                quiz_urls[quiz] = quiz.slug
            return render(request, "user_profile.html", context={"quizzes": quiz_urls,
                                                                 "viewing_user": user,
                                                                 "followings": followings,
                                                                 "completed_quizzes": completed_quizzes})

    raise Http404("User not found")

def user_quizzes(request, user_slug):
    try:
        viewing_user = UserProfile.objects.get(slug=user_slug).user
        created_quiz = Quiz.objects.filter(author__user_profile__slug=user_slug)
        completed_quiz = CompletedQuiz.objects.filter(user__user_profile__slug=user_slug)
        return render(request, "user_quizzes.html", context={"viewing_user": viewing_user,
                                                             "created_quiz": created_quiz,
                                                             "completed_quiz": completed_quiz})
    except:
        raise Http404("User not found")

def user_social(request, user_slug):
    try:
        viewing_user = UserProfile.objects.get(slug=user_slug).user
        followings = viewing_user.user_profile.following.order_by("username").all()
        followers = UserProfile.objects.filter(following__in=[viewing_user]).all()
        return render(request, "user_social.html", context={"viewing_user": viewing_user,
                                                             "followings": followings,
                                                             "followers": followers})
    except:
        raise Http404("User not found")

def create_quiz_page(request):
    
    if not request.user.is_authenticated:
        return redirect("Main:home_page")
    
    if request.method == "POST":
        quiz_info = json.loads(request.POST["quiz"])
        quiz_files = request.FILES
        
        if Quiz.objects.filter(slug=slugify(quiz_info["title"].strip()),
                               author=request.user).exists():
            messages.error(request, "You have already created a quiz of the same title.")
            return error_msg_response(request)

        quiz = Quiz.objects.create(title=quiz_info["title"].strip(),
                                   thumbnail=quiz_files["thumbnail"],
                                   media_quiz=quiz_info["media_quiz"],
                                   mcq=quiz_info["mcq"],
                                   author=request.user)
        
        quiz_questions = quiz_info["questions"]
        
        for item in quiz_questions:
            for question, question_info in item.items():
                
                correct_answers = []
                wrong_answers = []
                
                for correct_answer in question_info["correct"]:
                    answer, created = CorrectAnswer.objects.get_or_create(answer=correct_answer)
                    correct_answers.append(answer)
                
                for wrong_answer in question_info["wrong"]:
                    if wrong_answer == "": continue
                    answer, created = WrongAnswer.objects.get_or_create(answer=wrong_answer)
                    wrong_answers.append(answer)
                
                created_question = Question.objects.create(question=question)
                created_question.correct.set(correct_answers)
                created_question.wrong.set(wrong_answers)
                
                if quiz_info["media_quiz"]:
                    created_question.thumbnail = quiz_files[question_info["thumbnail"]]
                    created_question.save()
                    
                quiz.questions.add(created_question)

        messages.success(request, f"Successfully created the Quiz \"{quiz_info['title']}\"")
        
        data = {
                "quiz_url": f"/{request.user.user_profile.slug}/{quiz.slug}"
            }
                    
        response = HttpResponse(
            json.dumps(data),
            content_type="application/json",
        )
        response.status_code = 200
        return response
    
    return render(request, "create_quiz.html")

def edit_quiz_slug(request, user_slug, quiz_slug):

    if not request.user.is_authenticated:
        return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)
    try:
        user = UserProfile.objects.get(slug=user_slug).user
        if request.user != user:
            return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)
            
        try:
            quiz = Quiz.objects.get(slug=quiz_slug, author=user)

            if request.method == "POST":
                
                title = request.POST["title"].strip()
                
                if Quiz.objects.filter(slug=slugify(title), author=user).exists():
                    messages.error(request, f"You already have a quiz titled \"{title}\"")
                    return error_msg_response(request)
                    
                quiz.title = title
                
                if len(list(request.FILES)) > 0:
                    quiz.thumbnail = request.FILES["thumbnail"]
                    
                quiz.save()
                
                messages.success(request, f"Successfully updated quiz to \"{request.POST['title']}\"")
                data = {
                    "quiz_url": f"/{request.user.user_profile.slug}/{quiz.slug}"
                }
                    
                response = HttpResponse(
                    json.dumps(data),
                    content_type="application/json",
                )
                response.status_code = 200
                return response
                    
            return render(request, "edit_quiz.html", context={"quiz": quiz})
        except:
            raise Http404("Quiz not found")

    except:
        raise Http404("User not found")

def delete_quiz_slug(request, user_slug, quiz_slug):
    
    try:
        user = UserProfile.objects.get(slug=user_slug).user
    except:
        raise Http404("User not found")
    
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to do this.")
        return error_msg_response(request)
    
    if request.user != user:
        return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)
    
    if request.method == "DELETE":
        try:
            quiz = Quiz.objects.get(slug=quiz_slug, author=user)
            
            for question in quiz.questions.all():
                question.delete()
                
            quiz.delete()
            
            messages.success(request, f"Successfully deleted the quiz \"{quiz.title}\"")
            response = HttpResponse(200)
            response.status = 200
            return response
        except:
            messages.error(request, "An error has occured trying to do this.")
            return error_msg_response(request)
    else:
        return redirect("Main:user_quiz_slug", user_slug=user_slug, quiz_slug=quiz_slug)

def notifications_page(request):
    notifications = Notification.objects.filter(for_user=request.user).order_by("-pk")
    return render(request, "notifications.html", context={"notifications": notifications})

def notifications__read_delete(request, action):
    if not request.user.is_authenticated:
        return redirect("Main:notifications_page")
    
    notifications = Notification.objects.filter(for_user=request.user)
    
    for notification in notifications:
        if action == "read":
            notification.read = True
            notification.save()
        elif action == "delete":
            notification.delete()
        else:
            break
        
    return redirect("Main:notifications_page")

def notification_read(request, notification_id):
    if not request.user.is_authenticated:
        return redirect("Main:notifications_page")
    
    if request.method == "PUT":
        notification = Notification.objects.get(pk=notification_id)
        notification.read = not notification.read
        notification.save()
        
        return HttpResponse(status=204)
        
    return redirect("Main:notifications_page")

def handler404(request, exception):
    response = render(request, "errors/404.html", context={"exception": exception})
    return response