import datetime
from django.shortcuts import render, redirect

from homepage.models import chat, message, Offer
from django.contrib.auth.models import User
import datetime


# displays the chat with all of its messages
def Chat(request, offer_id, user_id):
    # finds or cretes the correct chat
    offer = Offer.objects.get(id=offer_id)
    user_2 = User.objects.get(id=user_id)
    if chat.objects.filter(
        offer_id=offer_id, user_1=request.user, user_2=user_2
    ).exists():
        chat_obj = chat.objects.get(
            offer_id=offer_id, user_1=request.user, user_2=user_2
        )
    elif chat.objects.filter(
        offer_id=offer_id, user_2=request.user, user_1=user_2
    ).exists():
        chat_obj = chat.objects.get(
            offer_id=offer_id, user_2=request.user, user_1=user_2
        )
    else:
        chat_obj = chat.objects.create(
            user_1=request.user, user_2=offer.creator, offer_id=offer_id
        )

    # creates a new message
    if request.method == "POST":
        if request.POST.get("message"):
            message.objects.create(
                chat=chat_obj,
                message_sender=request.user,
                message=request.POST.get("message"),
            )

    # context
    messages = message.objects.filter(chat=chat_obj)
    context = {
        "chat": chat_obj,
        "messages": messages,
    }
    return render(request, "chat/chat.html", context)
