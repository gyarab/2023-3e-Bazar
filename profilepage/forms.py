from django import forms
from homepage.models import Category, Order
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField

# the form used for making an order
class MakeAnOrder(forms.Form):
    title = forms.CharField(label="Title", max_length=255)
    description = RichTextUploadingFormField()
    category = forms.ModelChoiceField(Category.objects.all())
    price = forms.IntegerField()

# form used for adding users adress
class adress(forms.Form):
    City = forms.CharField(max_length=225)
    Street = forms.CharField(max_length=225)
    Postal_code = forms.CharField(max_length=225)

# used for deiting your offer description
class edit_description(forms.Form):
    description = RichTextUploadingFormField()
