import datetime
from django.shortcuts import render, redirect

from homepage.models import chat, message, Offer
from django.contrib.auth.models import User
import datetime


# displays the chat with all of its messages
def Chat(request, offer_id):
    # finds or cretes the correct chat
    order = Offer.objects.get(id=offer_id)
    if chat.objects.filter(offer_id=offer_id).exists():
        chat_obj = chat.objects.get(offer_id=offer_id)
    else:
        chat_obj = chat.objects.create(
            user_1=request.user, user_2=order.creator, offer_id=offer_id
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
