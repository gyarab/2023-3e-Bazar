from django import forms
from homepage.models import Order

class MakeAnOrder(forms.Form):

    class Meta:
        model = Order
        fields = ('Title', 'mail', '')
