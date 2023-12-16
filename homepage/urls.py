from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index),
    path('signup/', views.signup, name='signup'),
    path('<int:category_id>/', views.category, name='category'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
]