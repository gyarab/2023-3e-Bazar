from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    # path to the homepage
    path("", views.index, name="home"),
    # path to the order page
    path("order/<int:order_id>/", views.order, name="order"),
    # path to the signup page
    path("signup/", views.signup, name="signup"),
    # path to the login page
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    # simple paths for doing simple tasks
    path("logout/", views.out, name="logout"),
    path("theme/", views.theme, name="theme"),
]
