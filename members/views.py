from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUp
from django.contrib import messages
from .models import Members

# Create your views here.


# Login
def login_user(req):
    if req.method == "POST":
        email = req.POST["email"]
        password = req.POST["password"]

        user = authenticate(req, username=email, password=password)

        if user is not None and user.is_active:
            login(req, user)
            messages.success(req, "登入成功！")
            return redirect("home")
        else:
            messages.error(req, "登入失敗！")
            return redirect("login")
    else:
        return render(req, "registration/login.html")


# Logout
def logout_user(req):
    logout(req)
    messages.success(req, "登出成功！")
    return redirect("home")


# Register
def register_user(req):
    members = Members.objects.all()
    if req.method == "POST":
        form = SignUp(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "註冊成功！")
            return redirect("login")
        else:
            messages.error(req, "註冊失敗！")
            print(form.errors)
    else:
        form = SignUp()

    return render(req, "registration/register.html", {"form": form, "members": members})
