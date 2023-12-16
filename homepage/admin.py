from django.contrib import admin
from .models import Category, Order, OrderAttachment

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderAttachment)