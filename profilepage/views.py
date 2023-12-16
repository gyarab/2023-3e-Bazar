from django.shortcuts import render
from .forms import MakeAnOrder
from homepage.models import Order

def index(request):
    if request.method == 'POST': 
        u = MakeAnOrder(request.POST)

        if u.is_valid():
            title = u.cleaned_data["title"]
            description = u.cleaned_data["description"]
            category = u.cleaned_data["category"]
            phone_number = u.cleaned_data["phone_number"]
            
            o = Order.objects.create(
                Title = title,
                description = description,
                phone_number = phone_number,
                category = category,
                creator = request.user,
                mail = request.user.email,
            )
            o.save()

    form = MakeAnOrder()

    return render(request, 'profilepage/profilepage.html', {'form': form})
