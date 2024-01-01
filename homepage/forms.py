from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Jmeno uzivatele",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Heslo",
            }
        )
    )


class SignupForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Jmeno uzivatele",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email adresa",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Heslo",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Zopakujte heslo",
            }
        )
    )


class rate(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=10)
