"""Spuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

app_name = "Main"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("logout/", views.logout_page, name="log_out"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("settings/", views.settings_page, name="settings_page"),
    path("<user_slug>/", views.user_quiz_slug, name="user_slug"),
    path("<user_slug>/action/<action_slug>/", views.user_quiz_slug, name="action_slug"),
    path("<user_slug>/quizzes/", views.user_quizzes, name="user_quizzes"),
    path("<user_slug>/social/", views.user_social, name="user_social"),
    path("<user_slug>/<quiz_slug>/", views.user_quiz_slug, name="user_quiz_slug"),
]
