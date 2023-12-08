from django.shortcuts import redirect, render

from .forms import SignupForm

# Create your views here.

def index(request):
    return render(request, 'homepage.html')

def signup(request):
    if request.method == 'POST': 
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect('/login/')
    else:
        u = SignupForm()

    return render(request, 'signup.html', {'form' : u})