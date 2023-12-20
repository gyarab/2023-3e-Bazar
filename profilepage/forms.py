from django import forms
from homepage.models import Category, Order

class MakeAnOrder(forms.Form):
    title = forms.CharField(label="Title",max_length=40)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(Category.objects.all())
    price = forms.IntegerField()
    phone_number = forms.CharField(max_length=11)
    picture1 = forms.ImageField()
    picture2 = forms.ImageField()
    picture3 = forms.ImageField()
    picture4 = forms.ImageField()
