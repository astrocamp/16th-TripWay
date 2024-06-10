from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from PIL import Image
from io import BytesIO

from .forms import SignUp
from .models import MemberSpot, Member
from .models import MemberSpot
from trips.models import TripMember


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


def get_trip_data(member):
    trip_members = TripMember.objects.filter(member=member).select_related("trip")

    sort_option = 'created_desc'
    if sort_option == 'date_asc':
        trip_members = trip_members.order_by('trip__start_date')
    elif sort_option == 'date_desc':
        trip_members = trip_members.order_by('-trip__start_date')
    else:
        trip_members = trip_members.order_by('-trip__id')

    trips = [{"t": trip_member.trip, "tm": trip_member } for trip_member in trip_members]

    return trips


@login_required
def profile(request):
    member = request.user
    spots = MemberSpot.objects.filter(member=member).select_related("spot")
    trips = get_trip_data(member)

    context = {
        "spots": spots,
        "member": member,
        "trips": trips,
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