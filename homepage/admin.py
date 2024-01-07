from django.contrib import admin
from .models import (
    Category,
    Order,
    Theme,
    User_attachments,
    Rating_Relation,
)

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Theme)
admin.site.register(User_attachments)
admin.site.register(Rating_Relation)
