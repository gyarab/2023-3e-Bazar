from django import forms
from homepage.models import Category, Order


class MakeAnOrder(forms.Form):
    title = forms.CharField(label="Title", max_length=40)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(Category.objects.all())
    price = forms.IntegerField()
    phone_number = forms.CharField(max_length=11)


class Location(forms.Form):
    Country = forms.CharField(max_length=225)
    City = forms.CharField(max_length=225)
    Street = forms.CharField(max_length=225)
    Postal_code = forms.CharField(max_length=225)
