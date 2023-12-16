from django import forms
from homepage.models import Category, Order

class MakeAnOrder(forms.Form):

    title = forms.CharField(label="Title",max_length=40)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(Category.objects.all())
    phone_number = forms.CharField(max_length=11)