from django.urls import path
from . import views

urlpatterns = [
    # path to the respectiv chats
    path("<int:offer_id>/", views.Chat, name="chat"),
]
