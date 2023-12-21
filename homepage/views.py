from django.shortcuts import redirect, render, get_object_or_404

from .forms import SignupForm, LoginForm
from .models import Category, Order

# Create your views here.

def index(request):
    category = Category.objects.all()
    order = Order.objects.all()

    orders = []
    if 'search' in request.POST:
        searched = request.POST['searched_text']
        orders = Order.objects.filter(Title__contains=searched)
    else:
        orders = order

    context = {
        "category": category,
        "order": orders,
    }
    return render(request, 'home.html', context)

def category(request, category_id):
    c = get_object_or_404(Category, pk=category_id)
    order = Order.objects.filter(category__name=c.name)

    if 'search' in request.POST:
        searched = request.POST['searched_text']
        #TODO kategorizovanej search
        orders = Order.objects.filter(Title__contains=searched)
    else:
        orders = order

    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders,
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST': 
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect('/login/')
    else:
        u = SignupForm()

    return render(request, 'signup.html', {'form' : u})

def resetpassword(request):
    return render(request, 'resetpassword.html')

def logout(request):
    logout(request)
    return redirect('/login/')
    