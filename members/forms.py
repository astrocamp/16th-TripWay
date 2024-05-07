from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUp(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
            }
        ),
    )
    # email = forms.EmailField(
    #     label="電子郵件",
    #     widget=forms.EmailInput(
    #         attrs={
    #             "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
    #         }
    #     ),
    # )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
            }
        ),
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-72 px-2 py-2 border-2 rounded-lg focus:outline-none"
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
