from django.urls import path
from . import views

urlpatterns = [
    # path used for deleting an account
    path("delete/", views.delete, name="delete"),
    # path that leads to users personal info
    path("", views.personal_info, name="personal_info"),
    # path that leads to the page where users offers are listed
    path("offers/", views.offers, name="offers"),
    # this path is used for just refreshing youer offer after a month so that
    # it is displayed again
    path("refresh/<int:offer_id>", views.refresh, name="refresh"),
    # used for displaying the offer editing page
    path("offer/<int:offer_id>/", views.offer, name="offer"),
    # paypal
    # path to the html that confirms your payment
    path("confirmed/<int:offer_id>/", views.confirmed, name="confirmed"),
    # path to the html that tells you that your payment failed
    path("canceled/<int:offer_id>/", views.cancel, name="canceled"),
    # delete offer path
    path("delete/<int:offer_id>/", views.delete_offer, name="delete_offer"),
]
