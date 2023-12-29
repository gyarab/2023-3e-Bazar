from django.shortcuts import render
from .forms import MakeAnOrder
from homepage.models import Order, OrderAttachment

# fix the index method to actually save the order
def index(request):
    if request.method == 'POST': 
        u = MakeAnOrder(request.POST)

        if u.is_valid():
            #TODO fixnout - neuklada se to
            o = Order.objects.create(
                Title = u.cleaned_data["title"],
                description = u.cleaned_data["description"],
                phone_number = u.cleaned_data["category"],
                category = u.cleaned_data["phone_number"],
                price = u.cleaned_data["price"],
                creator = request.user,
                mail = request.user.email,
            )
            o.save()
            a = OrderAttachment.objects.create( 
                picture1 = u.cleaned_data["picture1"],
                picture2 = u.cleaned_data["picture2"],
                picture3 = u.cleaned_data["picture3"],
                picture4 = u.cleaned_data["picture4"],
                order = o,
            )
            a.save()

    form = MakeAnOrder()

    return render(request, 'profilepage/profilepage.html', {'form': form})