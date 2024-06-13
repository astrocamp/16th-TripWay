from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from notifies.models import Notification


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from PIL import Image
from io import BytesIO

from .forms import SignUp
from .models import MemberSpot
from trips.models import TripMember
import os
import qrcode
from base64 import b64encode


def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)

            create_welcome_notification(user)

            messages.success(request, "登入成功！")
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            return redirect("home")
        else:
            messages.error(request, "登入失敗！")
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
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
            user = form.save()
            create_welcome_notification(user)
            messages.success(request, "註冊成功！")
            return redirect("login")
        else:    
            messages.error(request, "註冊失敗！")
    else:
        form = SignUp()

    return render(request, "registration/register.html", {"form": form})


def get_trip_data(member, sort_option):
    trip_members = TripMember.objects.filter(member=member).select_related("trip")

    if sort_option == "date_asc":
        trip_members = trip_members.order_by("trip__start_date")
    elif sort_option == "date_desc":
        trip_members = trip_members.order_by("-trip__start_date")
    else:
        trip_members = trip_members.order_by("-trip__id")

    trips = [{"t": trip_member.trip, "tm": trip_member } for trip_member in trip_members]

    return trips


@login_required
def profile(request):
    member = request.user
    spots = MemberSpot.objects.filter(member=member).select_related("spot")
    sort_option = request.GET.get("sort", "created_desc")
    trips = get_trip_data(member, sort_option)

    if trips :
        for trip in trips :
            
            edit_url = f"https://{os.getenv("HOST_NAME")}/trips/{trip["t"].id}/add-member/edit"
            confirm_url = f"https://{os.getenv("HOST_NAME")}/trips/{trip["t"].id}/add-member/edit/confirm"
            watch_url = f"https://{os.getenv("HOST_NAME")}/trips/{trip["t"].id}/add-member/watch"

            content = {
                "id": trip["t"].id,
                "edit_url": edit_url,
                "confirm_url": confirm_url,
                "watch_url": watch_url,
                "confirm_qrimg" : create_qrcode(confirm_url),
                "watch_qrimg" : create_qrcode(watch_url)
            }
            
            trip['content'] = content

    context = {
        "spots": spots,
        "member": member,
        "trips": trips,
        "sort_option": sort_option,
    }

    return render(request, "profile/index.html", context)


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


def create_qrcode(url):
    qr_code_img = qrcode.make(url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    return qr_code_data


def create_welcome_notification(user):
    welcome_message = "歡迎加入TripWay，讓您一手掌握所有行程規劃需求，開始盡情享受獨一無二的冒險吧！"
    # 檢查使用者是否已經收到了歡迎通知
    if not Notification.objects.filter(user=user, message=welcome_message).exists():
        Notification.objects.create(
            user=user,
            message=welcome_message,
            type="welcome",
        )


@receiver(user_logged_in)
def handle_login(sender, request, user, **kwargs):
    if user.socialaccount_set.filter(provider="google").exists() or user.socialaccount_set.filter(provider="line").exists():
        create_welcome_notification(user)