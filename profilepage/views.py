from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import MakeAnOrder, adress, edit_description
from homepage.models import Order, User_attachments, Rating_Relation, chat, Category
from datetime import datetime
from django.conf import settings
import uuid
from django.urls import reverse

# TODO remove
from django.core.exceptions import ValidationError

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
    if request.method == "POST" and att.offer_count <= 4:
        u = MakeAnOrder(request.POST)
        if u.is_valid():
            o = Order.objects.create(
                Title=u.cleaned_data["title"],
                price=u.cleaned_data["price"],
                description = u.cleaned_data["description"],
                creation_date = datetime.now(),
                expired = False,
                creator = request.user,
                importance = 0,
                category = u.cleaned_data["category"],
            )
            o.save()
            att.offer_count += 1
            att.save()
            return redirect("/profilepage/offers/")

    form = MakeAnOrder()

    # used for checking if the user has added an adress
    # and if not, the form for adding an offer will not be displayed
    show_form = True
    if (
        att.City == ""
        or att.Street == ""
        or att.Postal_code == ""
        or att.phone_number == ""
    ):
        show_form = False

    # context
    context = {
        "form": form,
        "att": att,
        "orders": orders,
        "show": show_form,
    }
    return render(request, "profilepage/user_offers.html", context)

# displays the offer editing page
def offer(request, offer_id):
    # ! paypal
    host = request.get_host()

    # paypal checkout info
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

    # checks if your offer is expired and so if the renew button should be displayed
    expired = False
    if Order.objects.filter(pk=offer_id).filter(expired=True).exists():
        expired = True

    # used to edit users offers
    offer = Order.objects.get(pk=offer_id)
    if request.method == "POST":
        # title
        if request.POST.get("title"):
            offer.Title = request.POST.get("title")
            offer.save()
        # price
        if request.POST.get("price"):
            offer.price = request.POST.get("price")
            offer.save()
        # category
        if request.POST.get("category"):
            cat = Category.objects.get(pk=request.POST.get("category"))
            offer.category = cat
            offer.save()
    
    # used to edit user offer description
    if request.method == "POST":
        u = edit_description(request.POST)

        if u.is_valid():
            offer.description = u.cleaned_data["description"]
            offer.save()
            return redirect(f"/profilepage/offer/{offer_id}")
        
    # context
    description_edit_form = edit_description()

    category = Category.objects.all()
    # TODO escription_edit_form.description.data = offer.description
    att = User_attachments.objects.get(user=request.user)
    context = {
        "paypal": paypal_payment,
        "expired": expired,
        "offer_id": offer_id,
        "offer": offer,
        "category": category,
        "description_edit_form": description_edit_form,
        "att": att,
    }

    return render(request, "profilepage/your_order_detail.html", context)

# refreshes your offer 
def refresh(request, offer_id):
    order = Order.objects.get(pk=offer_id)

    order.creation_date = datetime.now()
    order.expired = False
    order.save()

    return redirect("/profilepage/offers/")

# if it is called adds to the importance to users offer
def confirmed(request, offer_id):
    order = Order.objects.get(pk=offer_id)

    order.importance += 3
    order.save()

    return render(request, "profilepage/payment_confirmed.html")

# is called when the paypal payment didnt go through
def cancel(request, offer_id):
    return render(request, "profilepage/payment_canceled.html")

# deletes the user and all of his attachments   
def delete(request):
    if request.user.is_authenticated:
        User_attachments.objects.get(user=request.user).delete()
        request.user.delete()
        logout(request)
    return redirect("/")

# takes care of deleting offers
def delete_offer(request, offer_id):
    Order.objects.get(pk=offer_id).delete()
    att = User_attachments.objects.get(user=request.user)
    att.offer_count -= 1
    att.save()
    return redirect("/profilepage/offers/")

    # ! important you can use this
    # ? important you can use this
    # hello
    # TODO todo
