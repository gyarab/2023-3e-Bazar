from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import MakeAnOrder, User_attachment, User_attachmentS
from homepage.models import Order, User_attachments, Rating_Relation, chat
from datetime import datetime

# paypal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


def personal_info(request):
    att = User_attachments.objects.get(user=request.user)

    if request.method == "POST":
        if request.POST.get("edit_phone_number"):
            att.phone_number = request.POST.get("edit_phone_number")
            att.save()
        if request.POST.get("edit_name"):
            user = request.user
            user.first_name = request.POST.get("edit_name")
            user.save()
        if request.POST.get("edit_surname"):
            user = request.user
            user.last_name = request.POST.get("edit_surname")
            user.save()
        if request.POST.get("edit_city"):
            att.City = request.POST.get("edit_city")
            att.save()
        if request.POST.get("edit_street"):
            att.Street = request.POST.get("edit_street")
            att.save()
        if request.POST.get("edit_postal"):
            att.Postal_code = request.POST.get("edit_postal")
            att.save()
        if request.POST.get("create_phone_number"):
            att.phone_number = request.POST.get("create_phone_number")
            att.save()

    form = User_attachmentS()

    if request.method == "POST":
        u = User_attachmentS(request.POST)

        if u.is_valid():
            att = User_attachments.objects.get(user=request.user)
            att.City = u.cleaned_data["City"]
            att.Street = u.cleaned_data["Street"]
            att.Postal_code = u.cleaned_data["Postal_code"]
            att.save()
            return redirect("/profilepage")

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


def offers(request):
    orders = Order.objects.filter(creator=request.user)

    att = User_attachments.objects.get(user=request.user)

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


def test(request, offer_id):
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


def out(request):
    logout(request)
    return redirect("/")


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
