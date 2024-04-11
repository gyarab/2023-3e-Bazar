from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    # path to the homepage
    path("", views.index, name="home"),
    # path to the offer page
    path("offer/<int:offer_id>/", views.offer, name="offer"),
    # path to the signup page
    path("signup/", views.signup, name="signup"),
    # path to the login page
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="homepage/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    # password reset
    path(
        "reset_password/",
        views.reset_password_custom,
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="homepage/reset_password_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="homepage/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="homepage/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # simple paths for doing simple tasks
    path("logout/", views.out, name="logout"),
    path("theme/", views.theme, name="theme"),
]
