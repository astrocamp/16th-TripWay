from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUp

# Create your views here.


# Login
def login_user(req):
    if req.method == "POST":
        email = req.POST["email"]
        password = req.POST["password"]

        user = authenticate(req, username=email, password=password)

        if user is not None and user.is_active:
            login(req, user)
            return redirect("home")
        else:
            return redirect("login")
    else:
        return render(req, "registration/login.html")


# Logout
def logout_user(req):
    logout(req)
    return redirect("home")


# Register
def register_user(req):
    if req.method == "POST":
        form = SignUp(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = SignUp()

    return render(req, "registration/register.html", {"form": form})
