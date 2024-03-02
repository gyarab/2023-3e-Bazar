from django.contrib import admin

from .models import (
    Category,
    Order,
    User_attachments,
    Rating_Relation,
    Feedback,
    chat,
    message,
)

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(User_attachments)
admin.site.register(Rating_Relation)
admin.site.register(Feedback)
admin.site.register(chat)
admin.site.register(message)
