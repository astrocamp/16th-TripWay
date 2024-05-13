from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member


class SignUp(UserCreationForm):
    # username = forms.CharField(required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none",
            }
        )
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
            "username": forms.TextInput(
                attrs={
                    "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
                }
            ),
        }
