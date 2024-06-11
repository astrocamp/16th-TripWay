from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from members.models import Member
from .models import Trip, TripMember
from notifies.models import Notification
from io import BytesIO
from base64 import b64encode
import qrcode
import os
from PIL import Image
from django.views.decorators.cache import cache_control

@login_required
def home(request):
    member = request.user
    trip_members = TripMember.objects.filter(member=member).select_related("trip")

    sort_option = request.GET.get('sort', 'created_desc')
    if sort_option == 'date_asc':
        trip_members = trip_members.order_by('trip__start_date')
    elif sort_option == 'date_desc':
        trip_members = trip_members.order_by('-trip__start_date')
    else:
        trip_members = trip_members.order_by('-trip__id')

    trips = [{"t": trip_member.trip, "tm": trip_member } for trip_member in trip_members]
    
    if trips :
        share_urls = []
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

        return render(request,"trips/index.html",{
            "trips": trips,
            "sort_option": sort_option,
            "share_urls" : share_urls,
            }   
        )
    else:
        return render(request,"trips/index.html",{"trips": trips,"sort_option": sort_option,})


@login_required
def new(request):
    return render(request, "trips/new.html")



@login_required
def new_member(request, id):
    trip = get_object_or_404(Trip, pk=id)
    return render(request, "trips/new_member.html", {"trip": trip})

@cache_control(public=True, max_age=3600)
def map(request):
    google_api_key = settings.GOOGLE_API_KEY
    return render(request, "trips/map.html", {"google_api_key": google_api_key})


@login_required
def create(request):
    if request.method == "POST":
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        transportation = request.POST["transportation"]
        image = request.FILES.get("image")
        
        if image :
            compressed_image_data = compress_image(image)
            image_name = "trips_coverPhoto/" + image.name
            image = default_storage.save(
                image_name, ContentFile(compressed_image_data.read())
            )
        
        checks = [
            (not name, "行程名稱不可為空"),
            (not start_date, "請選出發日期"),
            (not end_date, "請選結束日期"),
            (end_date < start_date, "結束日期不能早於開始日期"),
            (not transportation, "請選交通方式"),
        ]

        for condition, error_message in checks:
            if condition:
                messages.error(request, error_message)
                return render(request, "trips/new.html")

        member = request.user
        trip = Trip(
            name=name,
            start_date=start_date,
            end_date=end_date,
            transportation=transportation,
            owner=member.id,
            image=image,
        )

        trip.save()
        TripMember.objects.create(trip=trip, member=member, is_editable=True)


        Notification.objects.create(
            user = member, 
            message = f"成功創建新行程：{trip.name}",
            trip_id=trip.id,
            type="trip_creation",
            )

        messages.success(request, "旅程創建成功！")
        return redirect("trips:index")
    
    return render(request, "trips/new.html")


@login_required
def update(request, id):
    trip = get_object_or_404(Trip, pk=id)

    if request.method == "POST":
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        transportation = request.POST["transportation"]
        image = request.FILES.get("image")
        
        if image :
            compressed_image_data = compress_image(image)
            image_name = "trips_coverPhoto/" + image.name
            image = default_storage.save(
                image_name, ContentFile(compressed_image_data.read())
            )
            trip.image = image
            
        checks = [
            (not name, "行程名稱不可為空"),
            (not start_date, "請選擇出發日期"),
            (not end_date, "請選擇結束日期"),
            (end_date < start_date, "結束日期不能早於開始日期"),
            (not transportation, "請選交通方式"),
        ]

        for condition, error_message in checks:
            if condition:
                messages.error(request, error_message)
                return render(request, "trips/update.html", {"trip": trip})

        # 更新行程的資料
        trip.name = name
        trip.start_date = start_date
        trip.end_date = end_date
        trip.transportation = transportation

        trip.save()

        messages.success(request, "行程已更新！")
        return redirect("trips:index")

    return render(request, "trips/update.html", {"trip": trip})



@require_POST
@login_required
def create_member(request, id):
    trip = get_object_or_404(Trip, id=id)
    email = request.POST["email"]
    is_editable = request.POST["is_editable"] == "True"

    if email == request.user.email:
        messages.error(request, "不能添加自己為成員")
        return render(request, "trips/new_member.html", {"id": trip.id, "trip": trip})

    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        messages.error(request, "該電子郵件地址的用戶不存在")
        return render(request, "trips/new_member.html", {"id": trip.id, "trip": trip})

    TripMember.objects.create(trip=trip, member=member, is_editable=is_editable)
    trip.number += 1
    trip.save()
    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


@login_required
def new_member_edit(request, id):
    trip = get_object_or_404(Trip, id=id)
    member = request.user

    if (trip.owner != member.id):
        trip_member, created = TripMember.objects.get_or_create(
            trip=trip, member=member, defaults={"is_editable": True}
        )

        # 如果記錄已存在，更新
        if created:
            trip.number += 1
            trip.save()
        else:
            trip_member.is_editable = True
            trip_member.save()

    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


@login_required
def new_member_watch(request, id):
    trip = get_object_or_404(Trip, id=id)
    member = request.user

    if (trip.owner != member.id):
        trip_member, created = TripMember.objects.get_or_create(
            trip=trip, member=request.user, defaults={"is_editable": False}
        )

        # 如果記錄已存在，更新
        if created:
            trip.number += 1
            trip.save()
        else:
            trip_member.is_editable = False
            trip_member.save()

    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


def edit_confirm(request, id):
    trip = get_object_or_404(Trip, id=id)
    inviter = get_object_or_404(Member, id=trip.owner)
    return render(request, "trips/confirm.html", {"trip":trip, "inviter":inviter})

@require_POST
@login_required
def delete(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.delete()
    messages.success(request, "旅程刪除成功！")
    return redirect("trips:index")


def delete_TripMember(trip_id, member_id):
    trip_member = get_object_or_404(TripMember, trip_id=trip_id, member_id=member_id)
    trip_member.delete()
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.number -= 1
    trip.save()
    if trip.number == 0:
        trip.delete()


@require_POST
@login_required
def delete_member(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    messages.success(request, "成員刪除成功！")
    return redirect("trips:schedules:index", id=trip_id)


@require_POST
@login_required
def delete_self(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    return redirect("trips:index")


def create_qrcode(url):
    qr_code_img = qrcode.make(url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    return qr_code_data


def compress_image(image):
    img = Image.open(image)
    img.thumbnail((500, 500))
    output = BytesIO()
    img.save(output, format="PNG", quality=70)
    output.seek(0)
    return output
