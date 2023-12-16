from django.shortcuts import render
from .forms import MakeAnOrder
from homepage.models import Order, OrderAttachment

def index(request):
    if request.method == 'POST': 
        u = MakeAnOrder(request.POST)

        if u.is_valid():
            
            o = Order.objects.create(
                Title = u.cleaned_data["title"],
                description = u.cleaned_data["description"],
                phone_number = u.cleaned_data["category"],
                category = u.cleaned_data["phone_number"],
                creator = request.user,
                mail = request.user.email,
            )
            a = OrderAttachment.objects.create(
                picture1 = u.cleaned_data["picture1"],
                picture2 = u.cleaned_data["picture1"],
                picture3 = u.cleaned_data["picture1"],
                picture4 = u.cleaned_data["picture1"],
                order = o,
            )
            o.save()
            a.save()

    form = MakeAnOrder()

    return render(request, 'profilepage/profilepage.html', {'form': form})
