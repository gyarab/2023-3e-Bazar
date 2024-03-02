from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.index, name="home"),
    path("order/<int:order_id>/", views.order, name="order"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", views.out, name="logout"),
    path("theme/", views.theme, name="theme"),
]
