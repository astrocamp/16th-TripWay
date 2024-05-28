from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from itertools import groupby
from operator import attrgetter

from .models import Schedule
from spots.models import Spot
from members.models import Member
from trips.models import Trip, TripMember


@login_required
def index(request, id):
    google_api_key = settings.GOOGLE_API_KEY
    trip = get_object_or_404(Trip, pk=id)
    schedules = Schedule.objects.filter(trip=trip.id, deleted_at=None).order_by(
        "date", "start_time"
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
def add_day(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.end_date = trip.end_date + timedelta(days=1)
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
    if request.method == "POST":
        schedules.date = request.POST["date"]
        schedules.spot_name = request.POST["spot_name"]
        schedules.start_time = request.POST["start_time"]
        schedules.end_time = request.POST["end_time"]
        schedules.note = request.POST["note"]

        if schedules.end_time > schedules.start_time:
            schedules.save()
            messages.success(request, "更新成功！")
            return redirect("schedules:show", id=id)
        else:
            messages.error(request, "離開時間不可早於抵達時間！")
            return redirect("schedules:update", id=id)
    else:
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
        .select_related("spot")
        .values(
            "spot__latitude",
            "spot__longitude",
            "spot__name",
            "start_time",
            "date",
        )
        .order_by("date", "start_time")
    )
    return JsonResponse(list(schedule_data), safe=False)
