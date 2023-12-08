from django.shortcuts import render

from .forms import SignupForm

# Create your views here.

def index(request):
    return render(request, 'homepage.html')

def signup(request):
    u = SignupForm()

    return render(request, 'signup.html', {'form' : u})