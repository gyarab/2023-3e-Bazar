from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime, timedelta

from .forms import SignupForm, rate
from .models import Category, Order, Theme, Rating

#home
def index(request):

    color = ''
    if not request.user.is_anonymous and Theme.objects.filter(user=request.user).exists():
        color = Theme.objects.get(user=request.user).theme
    else:
        color = 'white'
        
    if 'filter' in request.POST or 'search' in request.POST:
        temp = useable2(request.POST.get('searched_text', ""), request.POST.get('category', 0), request.POST.get('price', 0))
        if not temp == 'failed':
            orders = temp
        else:
            orders = 'failed'
    else:
        orders = useable2("", 0, 0)

    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders,
        "color": color,
    }
    return render(request, 'home.html', context)

def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    color = ''
    if not request.user.is_anonymous and Theme.objects.filter(user=request.user).exists():
        color = Theme.objects.get(user=request.user).theme
    else:
        color = 'white'

    if request.method == 'POST': 
        u = rate(request.POST)

        if u.is_valid():
            userRating(order_id, u.cleaned_data['rating'])
    else:
        u = rate()

    context = {
        "order": order,
        "form": u,
        "color": color,
    }
    return render(request, 'order.html', context)

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

def profile():
    return redirect('/profilepage/')

def theme(request):
    color = request.GET.get('color')

    if color == 'light':
        if Theme.objects.filter(user=request.user).exists():
            theme = Theme.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = 'white'
            theme.save()
        else:
            theme = Theme()
            theme.user = request.user
            theme.theme = 'white'
            theme.save()
    elif color == 'dark':
        if Theme.objects.filter(user=request.user).exists():
            theme = Theme.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = 'grey'
            theme.save()
        else:
            theme = Theme()
            theme.user = request.user
            theme.theme = 'grey'
            theme.save()

    return redirect('/')


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
    
def useable2(searched, category_id, price):
    order = Order.objects.filter(expired=False)

    for o in order:
        if is_expired(o):
            order = order.exclude(pk=o.pk)

    if category_id == 0:
        pass
    else:
        c = get_object_or_404(Category, pk=category_id)
        for o in order:
            if not o.category == c:
                order = order.exclude(pk=o.pk)

    if not price == 0:
        for o in order:
            if o.price > int(price):
                order = order.exclude(pk=o.pk)
    
    if not searched == "":
        for o in order:
            if not o.Title.__contains__(searched):
                order = order.exclude(pk=o.pk)
    
    if order.count() == 0:
        return 'failed'
    else:
        return order


def userRating(order_id, rating):
    o = Order.objects.get(pk=order_id)
    user = o.creator
    if Rating.objects.filter(user=user).exists():
        r = Rating.objects.get(user=user)
        r.rating = (r.rating + rating) / 2
        r.save()
    else:
        r = Rating()
        r.user = user
        r.rating = rating
        r.save()
    
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