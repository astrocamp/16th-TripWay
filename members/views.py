from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUp
from .models import MemberSpot, Member
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


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


def logout_user(request):
    logout(request)
    messages.success(request, "登出成功！")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功！")
            return redirect("login")
        else:
            messages.error(request, "註冊失敗！")
    else:
        form = SignUp()

    return render(request, "registration/register.html", {"form": form})


def profile(request):
    member = request.user

    spots = MemberSpot.objects.filter(member=member).select_related("spot")
    return render(request, "profile/index.html", {"spots": spots, "member": member})


def create(request):
    member = request.user

    if request.method == "POST":
        if "image" in request.FILES:
            image = request.FILES["image"]
            compressed_image_data = compress_image(image)

            image_name = "member_profile/" + image.name
            image_path = default_storage.save(
                image_name, ContentFile(compressed_image_data.read())
            )

            member.image = image_path
            member.save()

    return redirect("profile")


def compress_image(image):
    img = Image.open(image)
    img.thumbnail((200, 200))
    output = BytesIO()
    img.save(output, format="PNG", quality=70)
    output.seek(0)
    return output
