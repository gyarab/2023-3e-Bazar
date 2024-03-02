from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import MakeAnOrder, adress
from homepage.models import Order, User_attachments, Rating_Relation, chat
from datetime import datetime
from django.conf import settings
import uuid
from django.urls import reverse

# paypal
from paypal.standard.forms import PayPalPaymentsForm

# personal info page
def personal_info(request):
    att = User_attachments.objects.get(user=request.user)

    # used for editing user details
    if request.method == "POST":
        # phone_number
        if request.POST.get("edit_phone_number"):
            att.phone_number = request.POST.get("edit_phone_number")
            att.save()
        # name
        if request.POST.get("edit_name"):
            user = request.user
            user.first_name = request.POST.get("edit_name")
            user.save()
        # surname
        if request.POST.get("edit_surname"):
            user = request.user
            user.last_name = request.POST.get("edit_surname")
            user.save()
        # city
        if request.POST.get("edit_city"):
            att.City = request.POST.get("edit_city")
            att.save()
        # street
        if request.POST.get("edit_street"):
            att.Street = request.POST.get("edit_street")
            att.save()
        # postal code
        if request.POST.get("edit_postal"):
            att.Postal_code = request.POST.get("edit_postal")
            att.save()
        # used for adding a phone number if it is not added
        if request.POST.get("create_phone_number"):
            att.phone_number = request.POST.get("create_phone_number")
            att.save()

    # used for adding an adress if it is not added
    form = adress()
    if request.method == "POST":
        u = adress(request.POST)

        if u.is_valid():
            att = User_attachments.objects.get(user=request.user)
            att.City = u.cleaned_data["City"]
            att.Street = u.cleaned_data["Street"]
            att.Postal_code = u.cleaned_data["Postal_code"]
            att.save()
            return redirect("/profilepage")

    # just context
    relation = Rating_Relation.objects.filter(rating_subject=request.user)

    chat_obj1 = chat.objects.filter(user_1=request.user)
    chat_obj2 = chat.objects.filter(user_2=request.user)

    context = {
        "att": att,
        "form": form,
        "relation": relation,
        "chat_obj1": chat_obj1,
        "chat_obj2": chat_obj2,
    }

    return render(request, "profilepage/personal_info.html", context)

# displays a offer creating form and your offers
def offers(request):
    orders = Order.objects.filter(creator=request.user)

    att = User_attachments.objects.get(user=request.user)

    # form for creating an offer
    form = None
    if request.method == "POST":
        u = MakeAnOrder(request.POST)

        if u.is_valid():
            o = Order()
            o.Title = u.cleaned_data["title"]
            o.price = u.cleaned_data["price"]
            o.description = u.cleaned_data["description"]
            o.creation_date = datetime.now()
            o.expired = False
            o.creator = request.user
            o.importance = 0
            o.category = u.cleaned_data["category"]
            o.save()
            return redirect("/offers")

    form = MakeAnOrder()

    show_form = True
    if (
        att.City == ""
        or att.Street == ""
        or att.Postal_code == ""
        or att.phone_number == ""
    ):
        show_form = False

    context = {
        "form": form,
        "att": att,
        "orders": orders,
        "show": show_form,
    }
    return render(request, "profilepage/user_offers.html", context)


def offer(request, offer_id):
    # ! paypal
    host = request.get_host()

    paypal_checkout = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10",
        "item_name": "zvyrazneni inzeratu",
        "invoice": uuid.uuid4(),
        "currency_code": "USD",
        "notify_url": f"https://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('confirmed', kwargs = {'offer_id': offer_id})}",
        "cancel_url": f"http://{host}{reverse('canceled', kwargs = {'offer_id': offer_id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    expired = False
    if Order.objects.filter(pk=offer_id).filter(expired=True).exists():
        expired = True

    context = {
        "paypal": paypal_payment,
        "expired": expired,
        "offer_id": offer_id,
    }

    return render(request, "profilepage/your_order_detail.html", context)

def refresh(request, offer_id):
    order = Order.objects.get(pk=offer_id)

    order.creation_date = datetime.now()
    order.expired = False
    order.save()

    return redirect("/profilepage/offers/")


def confirmed(request, offer_id):
    order = Order.objects.get(pk=offer_id)

    order.importance += 3
    order.save()

    return render(request, "profilepage/payment_confirmed.html")


def cancel(request, offer_id):
    return render(request, "profilepage/payment_canceled.html")


def delete(request):
    if request.user.is_authenticated:
        User_attachments.objects.get(user=request.user).delete()
        request.user.delete()
        logout(request)
    return redirect("/")

    # ! important you can use this
    # ? important you can use this
    # hello
    # TODO todo
