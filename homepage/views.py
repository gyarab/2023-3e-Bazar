from django.shortcuts import redirect, render, get_object_or_404

from .forms import SignupForm
from .models import Category, Order

# Create your views here.

def index(request):
    #categories
    category = [get_object_or_404(Category, pk=1)]
    for x in range (2, Category.objects.count() + 1):
        category.append(get_object_or_404(Category, pk=x))

    #orders
    order = [get_object_or_404(Order, pk=1)]
    for x in range (2, Order.objects.count() + 1):
        order.append(get_object_or_404(Order, pk=x))
    
    context = {
        "category": category,
        "order": order,
    }
    return render(request, 'homepage.html', context)

def category(request, category_id):
    category = [get_object_or_404(Category, pk=category_id)]
    
    context = {
        "category": category
    }
    return render(request, 'homepage.html', context)


def signup(request):
    if request.method == 'POST': 
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect('/login/')
    else:
        u = SignupForm()

    return render(request, 'signup.html', {'form' : u})