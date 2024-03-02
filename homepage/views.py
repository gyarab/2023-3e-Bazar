from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime, timedelta
import requests
import geopy.distance
from requests.structures import CaseInsensitiveDict
from django.core.mail import send_mail
from bs4 import BeautifulSoup

from .forms import SignupForm, rate
from .models import Category, Order, User_attachments, Rating_Relation


# homepage method
def index(request):
    # creates a user_att first time user logs in
    if (
        not request.user.is_anonymous
        and not User_attachments.objects.filter(user=request.user).exists()
    ):
        att = User_attachments()
        att.user = request.user
        att.save()
    color = "white"

    # takes care of switching between dark and light mode
    if (
        not request.user.is_anonymous
        and User_attachments.objects.filter(user=request.user).exists()
    ):
        color = User_attachments.objects.get(user=request.user).theme
    else:
        color = "white"

    # takes care of filtering
    if "filter" in request.POST:
        temp = useable(request)
        if not temp == "failed":
            orders = temp
        else:
            orders = "failed"
    else:
        orders = useable(request)

    # simple search
    if "search" in request.POST:
        orders = Order.objects.filter(Title__contains=request.POST["searched_text"])

        if orders.count() == 0:
            orders = "failed"

    # takes care of importance
    orders_imp = importance(orders)

    # takes care of deciding if the directions filter should be displayed
    display_directions = "dont-display"
    if not request.user.is_anonymous:
        att = User_attachments.objects.get(user=request.user)

        if not att.City == "" or not att.Street == "" or not att.Postal_code == "":
            display_directions = "display"
        else:
            display_directions = "dont-display"

    # just context
    category = Category.objects.all()
    context = {
        "category": category,
        "order": orders_imp,
        "color": color,
        "display_directions": display_directions,
    }

    # rendering the home.html
    return render(request, "home.html", context)


def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # takes care of switching between dark and light mode
    color = ""
    if (
        not request.user.is_anonymous
        and User_attachments.objects.filter(user=request.user).exists()
    ):
        color = User_attachments.objects.get(user=request.user).theme
    else:
        color = "white"

    # takes care of rating
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

    # just context
    relation = False
    if request.user.is_anonymous == False:
        if (
            Rating_Relation.objects.filter(rating_subject=order.creator)
            .filter(rating_creator=request.user)
            .exists()
        ):
            relation = True
    comments = Rating_Relation.objects.filter(rating_subject=order.creator)
    att = User_attachments.objects.get(user=order.creator)


    context = {
        "order": order,
        "form": u,
        "color": color,
        "rated": rated,
        "relation": relation,
        "comments": comments,
        "att": att,
    }
    return render(request, "order.html", context)


# takes care of creating accounts
def signup(request):
    if request.method == "POST":
        u = SignupForm(request.POST)

        if u.is_valid():
            u.save()

            return redirect("/login/")
    else:
        u = SignupForm()

    return render(request, "signup.html", {"form": u})


# simple method for loging out
def out(request):
    logout(request)
    return redirect("/")


# Takes care of switching between light and dark mode
def theme(request):
    color = request.GET.get("color")

    if color == "light":
        if User_attachments.objects.filter(user=request.user).exists():
            theme = User_attachments.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = "white"
            theme.save()
        else:
            theme = User_attachments()
            theme.user = request.user
            theme.theme = "white"
            theme.save()
    elif color == "dark":
        if User_attachments.objects.filter(user=request.user).exists():
            theme = User_attachments.objects.get(user=request.user)
            theme.user = request.user
            theme.theme = "black"
            theme.save()
        else:
            theme = User_attachments()
            theme.user = request.user
            theme.theme = "black"
            theme.save()

    return redirect("/")


# sorts the methods that should be displayed
def useable(request):
    order = Order.objects.filter(expired=False)

    # category
    if "category" in request.POST:
        category_id = request.POST["category"]
        if not category_id == "none":
            c = get_object_or_404(Category, pk=category_id)
            for o in order:
                if not o.category == c:
                    order = order.exclude(pk=o.pk)
    # keyword
    if "keyword" in request.POST:
        keyword = request.POST["keyword"]
        if not keyword == "":
            for o in order:
                if not o.Title.__contains__(keyword):
                    order = order.exclude(pk=o.pk)
    # price
    if "any-price" in request.POST:
        pass
    elif "0-1000-price" in request.POST:
        for o in order:
            if not o.price <= 1000:
                order = order.exclude(pk=o.pk)
    elif "1001-2500-price" in request.POST:
        for o in order:
            if not o.price > 1000 or not o.price <= 2500:
                order = order.exclude(pk=o.pk)
    elif "2501-5000-price" in request.POST:
        for o in order:
            if not o.price > 2500 or not o.price <= 5000:
                order = order.exclude(pk=o.pk)
    elif "5001-10000-price" in request.POST:
        for o in order:
            if not o.price > 5000 or not o.price <= 10000:
                order = order.exclude(pk=o.pk)
    elif "10000-more-price" in request.POST:
        for o in order:
            if not o.price > 10000:
                order = order.exclude(pk=o.pk)
    elif "min-price" in request.POST and "max-price" in request.POST:
        max = request.POST["max-price"]
        min = request.POST["min-price"]
        if not max == "" and not min == "":
            for o in order:
                if not o.price < int(max) or not o.price > int(min):
                    order = order.exclude(pk=o.pk)
    # distance
    if "distance" in request.POST:
        distance = request.POST["distance"]
        if not distance == "":
            for o in order:
                if not range(int(distance), request.user, o):
                    order = order.exclude(pk=o.pk)

    # figures out if the order is expired
    for o in order:
        k = Order.objects.get(pk=o.pk)
        if is_expired(k):
            order = order.exclude(pk=k.pk)

    # if some exist return them, if not return failed
    if order.count() == 0:
        return "failed"
    else:
        return order


# checks if a offer is too old
def is_expired(order):
    if order.creation_date.replace(tzinfo=None) < (datetime.now() - timedelta(days=30)):
        order.expired = True
        order.save()
        return True
    else:
        return False

# takes care of organazing offers so the ones that are paid to be propagaded
# actually are
def importance(orders):
    importance = []

    if orders != "failed":
        for order in orders:
            if order.importance > 0:
                importance.append(order)
                orders = orders.exclude(pk=order.pk)

    v = sorted(
        importance, key=lambda x: x.importance, reverse=True
    )  # TODO figure out wtf is this

    return v + list(orders)


# Takes care of calculating user rating
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


# takes care of searching by distance
def range(distance, user, order):
    att1 = User_attachments.objects.get(user=user)
    att2 = User_attachments.objects.get(user=order.creator)

    place1 = place_splitting(att1)
    place2 = place_splitting(att2)

    url1 = (
        "https://api.geoapify.com/v1/geocode/search?text="
        + place1
        + "&apiKey=7b75b8264118432ebc4643a8b88e7d67"
    )
    url2 = (
        "https://api.geoapify.com/v1/geocode/search?text="
        + place2
        + "&apiKey=7b75b8264118432ebc4643a8b88e7d67"
    )

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp1 = requests.get(url1, headers=headers)
    resp2 = requests.get(url2, headers=headers)

    data1 = resp1.json()
    data2 = resp2.json()

    lat1 = data1["features"][0]["properties"]["lat"]
    lon1 = data1["features"][0]["properties"]["lon"]
    lat2 = data2["features"][0]["properties"]["lat"]
    lon2 = data2["features"][0]["properties"]["lon"]

    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)

    v = geopy.distance.geodesic(coords_1, coords_2).km

    if v <= distance:
        return True
    else:
        return False

# formates the address for the api
def place_splitting(att):
    string = ""
    # city
    city = att.City.split()
    for c in city:
        string += c + "%20"
    string += "%2C%20"

    # street
    street = att.Street.split()
    for s in street:
        string += s + "%20"
    string += "%2C%20"

    # postal code
    postal = att.Postal_code.split()
    for p in postal:
        string += p + "%20"
    string += "%2C%20"

    string += "Czech%20Republic"

    return string


# Test method for generating test orders
# TODO nakonci smazat
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
