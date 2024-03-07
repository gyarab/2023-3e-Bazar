from django.contrib import admin

from .models import (
    Category,
    Offer,
    User_attachments,
    Rating_Relation,
    chat,
    message,
    payment,
)

admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(User_attachments)
admin.site.register(Rating_Relation)
admin.site.register(chat)
admin.site.register(message)
admin.site.register(payment)
