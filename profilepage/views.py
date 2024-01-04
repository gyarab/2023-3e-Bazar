from django.shortcuts import render, redirect
from .forms import MakeAnOrder, Location
from homepage.models import Order, OrderAttachment, User_attachments
from datetime import datetime


# fix the index method to actually save the order
def index(request):
    form1 = None
    form2 = None
    att = User_attachments.objects.get(user=request.user)
    if not att.Country == "":
        if request.method == "POST":
            u = MakeAnOrder(request.POST)

            if u.is_valid():
                # TODO fixnout - neuklada se to
                o = Order()
                o.Title = u.cleaned_data["title"]
                o.description = u.cleaned_data["description"]
                o.phone_number = u.cleaned_data["category"]
                o.category = u.cleaned_data["phone_number"]
                o.price = u.cleaned_data["price"]
                o.creation_date = datetime.now()
                o.expired = False
                o.creator = request.user
                o.mail = request.user.email
                o.save()
                a = OrderAttachment()
                a.picture1 = (u.cleaned_data["picture1"],)
                a.picture2 = (u.cleaned_data["picture2"],)
                a.picture3 = (u.cleaned_data["picture3"],)
                a.picture4 = (u.cleaned_data["picture4"],)
                a.order = o
                a.save()
                return redirect("/profilepage")

        form1 = MakeAnOrder()

    else:
        if request.method == "POST":
            u = Location(request.POST)

            if u.is_valid():
                att = User_attachments.objects.get(user=request.user)
                att.Country = u.cleaned_data["Country"]
                att.City = u.cleaned_data["City"]
                att.Street = u.cleaned_data["Street"]
                att.Postal_code = u.cleaned_data["Postal_code"]
                att.save()
                return redirect("/profilepage")

        form2 = Location()

    if form1:
        return render(request, "profilepage/profilepage.html", {"form1": form1})
    else:
        return render(request, "profilepage/profilepage.html", {"form2": form2})
