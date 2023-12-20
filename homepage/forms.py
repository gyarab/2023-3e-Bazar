from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Jmeno uzivatele',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Heslo',
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Jmeno uzivatele',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email adresa',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Heslo',
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zopakujte heslo',
    }))

        