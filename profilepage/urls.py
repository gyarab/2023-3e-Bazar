from django.urls import path
from . import views

urlpatterns = [
    path("delete/", views.delete, name="delete"),
    path("", views.personal_info, name="personal_info"),
    path("offers/", views.offers, name="offers"),
    path("logout/", views.out, name="logout"),
    path("confirmed/", views.confirmed, name="confirmed"),
    path("canceled/", views.cancel, name="canceled"),
    path("refresh/<int:offer_id>", views.refresh, name="refresh"),
    # test
    path("test/<int:offer_id>/", views.test, name="test"),
    path("confirmed/<int:offer_id>/", views.confirmed, name="confirmed"),
    path("canceled/<int:offer_id>/", views.cancel, name="canceled"),
]
