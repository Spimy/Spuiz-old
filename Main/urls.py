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
from django.urls import path, reverse_lazy
from django.conf.urls import url
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from . import views

app_name = "Main"

urlpatterns = [
    path("password-reset/", 
        PasswordResetView.as_view(template_name="password_reset/password_reset_form.html",
                                  email_template_name="password_reset/password_reset_email.html",
                                  success_url=reverse_lazy('Main:password_reset_done')),
        name="password_reset"),
    
    
    path("password-reset/done/", 
         PasswordResetDoneView.as_view(template_name="password_reset/password_reset_done.html"),
         name="password_reset_done"),
    
    
    path("password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset/password_reset_confirm.html",
            success_url=reverse_lazy('Main:password_reset_complete')
        ),
        name="password_reset_confirm"),
    
    path("password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete"),
    
    path("", views.home_page, name="home_page"),
    path("logout/", views.logout_page, name="log_out"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("settings/", views.settings_page, name="settings_page"),
    path("notifications/", views.notifications_page, name="notifications_page"),
    path("notifications/<action>/", views.notifications__read_delete, name="notifications__read_delete"),
    path("notifications/<notification_id>/read/", views.notification_read, name="notification_read"),
    path("search/", views.search_page, name="search_page"),
    path("create-quiz/", views.create_quiz_page, name="create_quiz_page"),
    path("<user_slug>/", views.user_profile, name="user_profile"),
    path("<user_slug>/quizzes/", views.user_quizzes, name="user_quizzes"),
    path("<user_slug>/social/", views.user_social, name="user_social"),
    path("<user_slug>/action/<action>/", views.user_action, name="user_action"),
    path("<user_slug>/<quiz_slug>/", views.quiz_page, name="quiz_page"),
    path("<user_slug>/<quiz_slug>/edit/", views.edit_quiz_slug, name="edit_quiz_slug"),
    path("<user_slug>/<quiz_slug>/delete/", views.delete_quiz_slug, name="delete_quiz_slug"),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate, name='activate'),
]
