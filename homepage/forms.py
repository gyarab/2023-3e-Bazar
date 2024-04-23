from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# form used for users login in
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Jmeno přes které vás oslovujeme",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Vaše bezpečné heslo",
            }
        )
    )

# form used for users registration
# Captcha taken from https://www.youtube.com/watch?v=8rWXdkUn3PM
class SignupForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Jmeno uzivatele aneb jmeno, kterým vás budeme oslovovat",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Emailová adresa přes kterou vás budeme kontaktovat",
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

# simple form used for rating users
class rate(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=10)
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Komentář",
            }
        )
    )
