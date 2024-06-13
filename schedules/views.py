from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import json
from datetime import timedelta
from itertools import groupby
from operator import attrgetter

from .models import Schedule
from spots.models import Spot
from members.models import Member
from trips.models import Trip, TripMember


@cache_control(public=True, max_age=3600)
@login_required
def index(request, id):
    google_api_key = settings.GOOGLE_API_KEY
    trip = get_object_or_404(Trip, pk=id)
    schedules = Schedule.objects.filter(trip=trip.id, deleted_at=None).order_by(
        "order", "date", "start_time"
    )

    grouped_schedules = {}
    # 根據行程的日期屬性將行程分組並提取日期
    for date, group in groupby(schedules, key=attrgetter("date")):
        grouped_schedules[date] = list(group)

    date_range = trip.get_date_range()
    member_ids = (
        TripMember.objects.filter(trip_id=id)
        .order_by("id")
        .values_list("member_id", flat=True)
    )
    members = Member.objects.filter(id__in=member_ids)
    trip_member = get_object_or_404(TripMember, trip=trip, member=request.user)

    return render(
        request,
        "schedules/index.html",
        {
            "schedule_dates": grouped_schedules,
            "date_range": date_range,
            "trip": trip,
            "members": members,
            "trip_member": trip_member,
            "google_api_key": google_api_key,
        },
    )


@require_POST
@login_required
def update_schedule_order(request):
    data = json.loads(request.body)
    updated_orders = data.get("updatedOrders", [])

    if not updated_orders:
        return JsonResponse({"success": False, "message": "無有效行程更新數據"})

    try:
        for update_data in updated_orders:
            schedule_id = update_data.get("id")
            order = update_data.get("order")
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.order = order
            schedule.save()
        return JsonResponse({"success": True})
    except Schedule.DoesNotExist:
        return JsonResponse({"success": False, "message": "行程不存在"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@require_POST
@login_required
def add_day(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.end_date = trip.end_date + timedelta(days=1)
    trip.save()
    return redirect(f"/trips/{trip.id}/schedules/")


@require_POST
@login_required
def delete_day(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.end_date = trip.end_date - timedelta(days=1)
    trip.save()
    return redirect(f"/trips/{trip.id}/schedules/")


@require_POST
@login_required
def create(request):
    trip_id = request.POST.get("trip_id")
    trip = get_object_or_404(Trip, id=trip_id)

    spot_id = request.POST.get("spot_id")
    spot = get_object_or_404(Spot, id=spot_id)

    schedules = Schedule(
        date=request.POST["day"],
        spot_name=request.POST["spot_name"],
        start_time=None,
        end_time=None,
        note="",
        trip=trip,
        spot=spot,
    )
    schedules.save()
    return redirect(f"/trips/{trip.id}/schedules/")


@login_required
def show(request, id):
    schedules = get_object_or_404(Schedule, pk=id)
    trip = schedules.trip
    trip_member = get_object_or_404(TripMember, trip=trip, member=request.user)
        
    return render(
        request,
        "schedules/show.html",
        {"schedules": schedules, "trip": trip, "trip_member": trip_member},
    )


@login_required
def update(request, id):
    schedule = get_object_or_404(Schedule, pk=id)

    date_range = schedule.trip.get_date_range()
    trip_member = get_object_or_404(TripMember, trip=schedule.trip, member=request.user)
    if not trip_member.is_editable:
        messages.error(request, "您沒有權限編輯此行程！")
        return redirect("home")

    if request.method == 'POST':
        date = request.POST["date"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        note = request.POST["note"]

        checks = [
            (not date, "請選擇行程日期"),
            (not start_time, "請選擇抵達時間"),
            (not end_time, "請選擇離開時間"),
            (end_time < start_time, "離開時間不可早於抵達時間！"),
        ]

        for condition, error_message in checks:
            if condition:
                messages.error(request, error_message)
                return redirect("schedules:update", id=id)

        # 更新行程資訊
        schedule.date = date
        schedule.start_time = start_time
        schedule.end_time = end_time
        schedule.note = note
        schedule.save()

        messages.success(request, "更新成功！")
        return redirect("trips:schedules:index", id=schedule.trip_id)

    return render(
        request,
        "schedules/update.html",
        {"schedule": schedule, "date_range": date_range},
    )


@login_required
@require_POST
def delete(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    schedule.deleted_at = timezone.now()
    schedule.save()
    messages.success(request, "成功刪除行程！")
    return redirect("trips:schedules:index", id=schedule.trip_id)


@login_required
def get_schedule(request):
    schedule_data = (
        Schedule.objects.filter(deleted_at__isnull=True)
        .select_related("spot", "trips")
        .values(
            "spot__latitude",
            "spot__longitude",
            "updated_at",
            "spot__name",
            "start_time",
            "date",
            "trip_id",
            "trip__transportation",
            "order",
        )
        .order_by("order", "date", "start_time", "updated_at")
    )
    return JsonResponse(list(schedule_data), safe=False)
