from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member


DEFAULT_STYLE = "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"


class SignUp(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": DEFAULT_STYLE})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": DEFAULT_STYLE})
    )

    class Meta:
        model = Member
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "帳號",
            "email": "信箱",
            "password1": "密碼",
            "password2": "密碼確認",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": DEFAULT_STYLE}),
            "email": forms.EmailInput(attrs={"class": DEFAULT_STYLE}),
            "password1": forms.PasswordInput(attrs={"class": DEFAULT_STYLE}),
            "password2": forms.PasswordInput(attrs={"class": DEFAULT_STYLE}),
        }
