from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUp
from django.contrib import messages
from .models import Members, Spot


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


# member profile index
def index(request, id):
    pass


def add_favorite_spot(request, member_id, spot_id):
    # 獲取會員對象和景點對象，如果不存在則返回404錯誤
    member = get_object_or_404(Members, pk=member_id)
    spot = get_object_or_404(Spot, pk=spot_id)
    
    # 使用 add() 方法將會員與景點關聯起來
    member.favorite_spots.add(spot)
    
    # 返回適當的響應，例如重定向到一個新的頁面或者返回一個成功消息
    return redirect("index")
