import datetime
from django.shortcuts import render, redirect

from homepage.models import chat, message, Order
from django.contrib.auth.models import User
import datetime


def Chat(request, order_id):
    order = Order.objects.get(id=order_id)
    if chat.objects.filter(order_id=order_id).exists():
        chat_obj = chat.objects.get(order_id=order_id)
    else:
        chat_obj = chat.objects.create(
            user_1=request.user, user_2=order.creator, order_id=order_id
        )

    if request.method == "POST":
        if request.POST.get("message"):
            message.objects.create(
                chat=chat_obj,
                message_sender=request.user,
                message=request.POST.get("message"),
            )

    messages = message.objects.filter(chat=chat_obj)

    context = {
        "chat": chat_obj,
        "messages": messages,
    }
    return render(request, "chat/chat.html", context)
