import boto3
from botocore.exceptions import NoCredentialsError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Trip, TripMember
from members.models import Member
from django.contrib import messages
from .models import Trip, Photo
from .forms import UploadModelForm
from django.conf import settings

# 列出目前行程
def home(request):
    member = request.user
    trip_members = TripMember.objects.filter(member=member)
    trip_ids = trip_members.values_list("trip_id", flat=True)
    trips = [{"t":trip, "tm":trip_members.get(trip=trip)} for trip in Trip.objects.filter(id__in=trip_ids).order_by("start_date")]
    return render(request, "trips/index.html", {"trips": trips})


# 輸入行程資訊
def new(request):
    return render(request, "trips/new.html")


def new_member(request, id):
    trip = get_object_or_404(Trip, pk=id)
    return render(request, "trips/new_member.html", {"trip": trip})


# google map
def map(request):
    return render(request, "trips/map.html")


def create(request):
    if request.method == "POST":
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        transportation = request.POST["transportation"]

        if end_date < start_date:
            messages.error(request, "結束日期不能早於開始日期")
            return redirect("trips:new") 

        member = request.user
        trip = Trip(
            name=name,
            start_date=start_date,
            end_date=end_date,
            transportation=transportation,
            owner=member.id
        )
        trip.save()
        TripMember.objects.create(trip=trip, member=member, is_editable=True)
        messages.success(request, "旅程創建成功！")
        return redirect("trips:index")


@require_POST
def create_member(request, id):
    trip = get_object_or_404(Trip, id=id)
    email = request.POST["email"]
    is_editable = (request.POST["is_editable"] == "True")
    member = get_object_or_404(Member, email=email)
    TripMember.objects.create(trip=trip, member=member, is_editable=is_editable)
    trip.number += 1
    trip.save()
    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


# 刪除行程(硬刪)
@require_POST
def delete(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.delete()
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
def delete_member(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    return redirect("trips:schedules:index", id=trip_id)


@require_POST
def delete_self(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    return redirect("trips:index")

# 新增圖片功能
def upload_photo(request):
    form = UploadModelForm()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        breakpoint()
        if form.is_valid():
            # 保存表单数据到数据库
            form.save()

            # 将图片上传到 AWS S3
            try:
                upload_to_s3(
                    request.FILES['image/'],  # 从请求中获取上传的图片文件
                    settings.AWS_STORAGE_BUCKET_NAME,  # 存储桶名称
                    f"photos/{request.FILES['image'].name}"  # 对象名称，使用图片文件名作为对象名称
                )
            except Exception as e:
                print("Failed to upload image to S3:", e)

            return redirect("trips:new")
    photos = Photo.objects.all()  # 从数据库中获取所有图片数据
    context = {
        'photos': photos,
        'form': form
    }
    return render(request, 'trips/new.html', context)

def upload_to_s3(file, bucket_name, object_name):
    # 创建 S3 客户端
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    try:
        # 将文件上传到 S3 存储桶中
        response = s3_client.upload_fileobj(file, bucket_name, object_name)
        print("Upload successful")
        return True
    except NoCredentialsError:
        print("AWS credentials not available")
        return False
