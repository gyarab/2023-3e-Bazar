from django import forms
from homepage.models import Category, Order
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# the form used for making an order
class MakeAnOrder(forms.Form):
    title = forms.CharField(label="Title", max_length=40)
    description = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ModelChoiceField(Category.objects.all())
    price = forms.IntegerField()

# form used for adding users adress
class adress(forms.Form):
    City = forms.CharField(max_length=225)
    Street = forms.CharField(max_length=225)
    Postal_code = forms.CharField(max_length=225)
