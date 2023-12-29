from django.contrib import admin
from .models import Category, Order, OrderAttachment, Theme, Rating

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderAttachment)
admin.site.register(Theme)
admin.site.register(Rating)