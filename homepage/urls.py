from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('<int:category_id>/', views.category, name='category'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('send-welcome-email/', views.send_welcome_email, name='send_welcome_email'),
]