from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from trips.models import Trip, TripMember
from .models import Schedule
from datetime import timedelta
from itertools import groupby
from operator import attrgetter
from members.models import Member
from spots.models import Spot

@login_required
def index(request, id):
    trip = get_object_or_404(Trip, pk=id)
    schedules = Schedule.objects.filter(trip=trip.id, deleted_at=None).order_by("date", "start_time")

    grouped_schedules = {}
    # 根據行程的日期屬性將行程分組並提取日期
    for date, group in groupby(schedules, key=attrgetter("date")):
        grouped_schedules[date] = list(group)

    date_range = trip.get_date_range()
    member_ids = TripMember.objects.filter(trip_id=id).order_by("id").values_list("member_id", flat=True)
    members = Member.objects.filter(id__in=member_ids)
    trip_member = get_object_or_404(TripMember, trip=trip, member=request.user)
    
    return render(
        request, "schedules/index.html", {
            "schedule_dates": grouped_schedules, 
            "date_range": date_range, 
            "trip": trip, "members": members, 
            "trip_member": trip_member
        }
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
        note=None,
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
        return render(request, "schedules/show.html", {
            "schedules": schedules, 
            "trip": trip, 
            "trip_member": trip_member
        })


@login_required
def update(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    date_range = schedule.trip.get_date_range()
    return render(
        request, "schedules/update.html",
        {"schedule": schedule, "date_range": date_range},
    )


@login_required
@require_POST
def delete(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    schedule.deleted_at = timezone.now()
    schedule.save()
    return redirect("trips:schedules:index", id=schedule.trip_id)
