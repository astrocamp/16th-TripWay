from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUp
from django.contrib import messages
from .models import Members

# Create your views here.


# Login
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, "登入成功！")
            return redirect("home")
        else:
            messages.error(request, "登入失敗！")
            return redirect("login")
    else:
        return render(request, "registration/login.html")


# Logout
def logout_user(request):
    logout(request)
    messages.success(request, "登出成功！")
    return redirect("home")


# Register
def register_user(request):
    members = Members.objects.all()
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功！")
            return redirect("login")
        else:
            messages.error(request, "註冊失敗！")
            print(form.errors)
    else:
        form = SignUp()

    return render(request, "registration/register.html", {"form": form, "members": members})
