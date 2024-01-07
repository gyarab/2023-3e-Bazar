from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime, timedelta
import requests
import json

from .forms import SignupForm, rate
from .models import Category, Order, Theme, User_attachments, Rating_Relation


# home
def index(request):
    if (
        not request.user.is_anonymous
        and not User_attachments.objects.filter(user=request.user).exists()
    ):
        att = User_attachments()
        att.user = request.user
        att.save()
    color = ""
    if (
        not request.user.is_anonymous
        and Theme.objects.filter(user=request.user).exists()
    ):
        color = Theme.objects.get(user=request.user).theme
    else:
        color = "white"

    if "filter" in request.POST or "search" in request.POST:
        temp = useable(
            request.POST.get("searched_text", ""),
            request.POST.get("category", 0),
            request.POST.get("price", 0),
        )
        if not temp == "failed":
            orders = temp
        else:
            orders = "failed"
    else:
        orders = useable("", 0, 0)

    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders,
        "color": color,
    }
    return render(request, "home.html", context)


def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Test - mozna se bude hodit - https://www.youtube.com/watch?v=7lhlXDHks_s = oba dili
    # ip1 = requests.get("https://api.ipify.org?format=json")
    # ip_data = json.loads(ip1.text)
    # res1 = requests.get("http://ip-api.com/json/" + ip_data["ip"])
    # d1 = res1.text
    # data1 = json.loads(d1)

    color = ""
    if (
        not request.user.is_anonymous
        and Theme.objects.filter(user=request.user).exists()
    ):
        color = Theme.objects.get(user=request.user).theme
    else:
        color = "white"

    rated = ""
    if request.method == "POST":
        u = rate(request.POST)

        if u.is_valid():
            rated = userRating(
                order_id,
                u.cleaned_data["rating"],
                u.cleaned_data["comment"],
                request.user,
            )
    else:
        u = rate()

    comments = Rating_Relation.objects.filter(rating_subject=order.creator)

    context = {
        "order": order,
        "form": u,
        "color": color,
        "rated": rated,
        "comments": comments,
    }
    return render(request, "order.html", context)


def signup(request):
    if request.method == "POST":
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect("/login/")
    else:
        u = SignupForm()

    return render(request, "signup.html", {"form": u})


def out(request):
    logout(request)
    return redirect("/")


def delete(request):
    if request.user.is_authenticated:
        User_attachments.objects.get(user=request.user).delete()
        request.user.delete()
        logout(request)
    return redirect("/")


def profile(request):
    return redirect("/profilepage/")


def theme(request):
    color = request.GET.get("color")

    if color == "light":
        if Theme.objects.filter(user=request.user).exists():
            theme = Theme.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = "white"
            theme.save()
        else:
            theme = Theme()
            theme.user = request.user
            theme.theme = "white"
            theme.save()
    elif color == "dark":
        if Theme.objects.filter(user=request.user).exists():
            theme = Theme.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = "grey"
            theme.save()
        else:
            theme = Theme()
            theme.user = request.user
            theme.theme = "grey"
            theme.save()

    return redirect("/")


def is_expired(order):
    if order.creation_date.replace(tzinfo=None) < (datetime.now() - timedelta(days=30)):
        order.expired = True
        order.save()
        return True
    else:
        return False


def useable(searched, category_id, price):
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
        return "failed"
    else:
        return order


def userRating(order_id, rating, comment, creator):
    o = Order.objects.get(pk=order_id)
    subject = o.creator

    relations = Rating_Relation.objects.filter(rating_subject=subject).filter(
        rating_creator=creator
    )
    if relations.exists():
        return "failed"
    else:
        if User_attachments.objects.filter(user=subject).exists():
            r = User_attachments.objects.get(user=subject)
            r.rating = (r.rating + rating) / 2
            r.save()
        else:
            r = User_attachments()
            r.user = subject
            r.rating = rating
            r.save()

        relation = Rating_Relation()
        relation.comment = comment
        relation.rating_subject = subject
        relation.rating_creator = creator
        relation.save()
        return "success"


# Test
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
