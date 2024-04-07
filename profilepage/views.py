from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import MakeAnOffer, adress, edit_description
from homepage.models import (
    Offer,
    User_attachments,
    Rating_Relation,
    chat,
    Category,
    payment,
)
from datetime import datetime
from django.conf import settings
import uuid
from django.urls import reverse
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required


# paypal
from paypal.standard.forms import PayPalPaymentsForm


# personal info page
@login_required
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
@login_required
def offers(request):

    # deletes all of request users uncompleted payments
    if payment.objects.filter(user=request.user, completed=False).exists():
        p = payment.objects.filter(user=request.user, completed=False).delete()

    offers = Offer.objects.filter(creator=request.user)

    att = User_attachments.objects.get(user=request.user)

    # form for creating an offer
    form = None
    if request.method == "POST" and att.offer_count <= 4:
        u = MakeAnOffer(request.POST)
        if u.is_valid():
            o = Offer.objects.create(
                Title=u.cleaned_data["title"],
                price=u.cleaned_data["price"],
                description=u.cleaned_data["description"],
                creation_date=datetime.now(),
                expired=False,
                creator=request.user,
                importance=0,
                category=u.cleaned_data["category"],
                preview=getImage(u.cleaned_data["description"]),
            )
            o.save()
            att.offer_count += 1
            att.save()
            return redirect("/profilepage/offers/")

    form = MakeAnOffer()

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
        "offers": offers,
        "show": show_form,
    }
    return render(request, "profilepage/user_offers.html", context)


# displays the offer editing page
@login_required
def offer(request, offer_id):

    # checks if your offer is expired and so if the renew button should be displayed
    expired = False
    if Offer.objects.filter(pk=offer_id).filter(expired=True).exists():
        expired = True

    # used to edit users offers
    offer = Offer.objects.get(pk=offer_id)
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
            return redirect(f"/profilepage/edit_offer/{offer_id}/")

    # context
    description_edit_form = edit_description()

    category = Category.objects.all()
    # TODO escription_edit_form.description.data = offer.description
    att = User_attachments.objects.get(user=request.user)
    context = {
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
    offer = Offer.objects.get(pk=offer_id)

    offer.creation_date = datetime.now()
    offer.expired = False
    offer.save()

    return redirect("/profilepage/offers/")


# if it is called adds to the importance to users offer
@login_required
def confirmed(request, payment_id):
    p = payment.objects.get(cid=payment_id)
    o = p.order

    if payment.objects.filter(cid=payment_id).exists():
        p.completed = True
        p.save()
        o.importance += 3
        o.save()

    return render(request, "profilepage/payment_confirmed.html")


# is called when the paypal payment didnt go through
@login_required
def cancel(request, offer_id):
    return render(request, "profilepage/payment_canceled.html")

@login_required
def payment_redirect(request, offer_id):
    id = uuid.uuid4()
    payment.objects.create(
        user=request.user,
        order=Offer.objects.get(pk=offer_id),
        cid=id,
    )
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
        "return_url": f"http://{host}{reverse('confirmed', kwargs = {'payment_id': id})}",
        "cancel_url": f"http://{host}{reverse('canceled', kwargs = {'payment_id': id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    att = User_attachments.objects.get(user=request.user)
    context = {
        "paypal": paypal_payment,
        "att": att,
    }
    return render(request, "profilepage/payment_confirmation.html", context)


# deletes the user and all of his attachments
def delete(request):
    if request.user.is_authenticated:
        User_attachments.objects.get(user=request.user).delete()
        request.user.delete()
        logout(request)

    return redirect("/")


# takes care of deleting offers
def delete_offer(request, offer_id):
    Offer.objects.get(pk=offer_id).delete()
    att = User_attachments.objects.get(user=request.user)
    att.offer_count -= 1
    if chat.objects.filter(offer_id=offer_id).exists():
        chat.objects.get(offer_id=offer_id).delete()
    att.save()
    return redirect("/profilepage/offers/")


# used to get the first image of the description
def getImage(html):
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img")
    if img is None:
        return "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg"
    else:
        return img["src"]
