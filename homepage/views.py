from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime, timedelta

from .forms import SignupForm
from .models import Category, Order

#home
def index(request):

    orders = []
    if 'search' in request.POST:
        orders = useable(request.POST['searched_text'], 0)
    else:
        orders = useable("", 0)

    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders,
    }
    return render(request, 'home.html', context)

#categories
def category(request, category_id):

    if 'search' in request.POST:
        orders = useable(request.POST['searched_text'], category_id)
    else:
        orders = useable("", category_id)

    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders,
    }
    return render(request, 'home.html', context)

#signup
def signup(request):
    if request.method == 'POST': 
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect('/login/')
    else:
        u = SignupForm()

    return render(request, 'signup.html', {'form' : u})

def out(request):
    logout(request)
    return redirect('/')

def profile(request):
    return redirect('/profilepage/')


#checks for legit orders
def useable(searched, category_id):
    if category_id == 0:
        order = Order.objects.filter(expired=False)
    else:
        c = get_object_or_404(Category, pk=category_id)
        order = Order.objects.filter(category__name=c.name).filter(expired=False)
    
    orders = []
    for o in order:
        if o.Title.__contains__(searched) and not is_expired(o):
            orders.append(o)
        elif searched == "" and not is_expired(o):
            orders.append(o)

    return orders
    
def is_expired(order):
    if order.creation_date.replace(tzinfo=None) < (datetime.now() - timedelta(days=30)):
        order.expired = True
        order.save()
        return True
    else:
        return False
    
#Test
def generate(request):
    Order.objects.all().delete()
    for i in range(100):
        o = Order()
        o.Title = "Test" + str(i)
        o.mail = "test" + str(i) + "@test.com"
        o.price = i
        o.phone_number = "123456789"
        o.description = "test"
        o.creation_date = datetime.now() + timedelta(days=30)
        o.expired = False
        o.creator = request.user
        o.category = Category.objects.get(pk=1)
        o.save()
    
