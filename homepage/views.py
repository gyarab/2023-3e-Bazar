from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from django.core.mail import send_mail

from .forms import SignupForm
from .models import Category, Order

#home
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

#categories
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

#TODO smazat nebo dodelat
def send_welcome_email(request):
    subject = 'Vítejte na našem bazaru'
    message = 'Děkujeme za vytvoření účtu!'
    from_email = 'admin@mysite.com'
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)
    return redirect('/login/')

def out(request):
    logout(request)
    return redirect('/')

def profile(request):
    return redirect('/profilepage/')