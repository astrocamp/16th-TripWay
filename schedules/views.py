from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Schedule
from trips.models import Trip, TripMember
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from itertools import groupby
from operator import attrgetter
from members.models import Member
from spots.models import Spot

def index(request, id):
    trip = get_object_or_404(Trip, pk=id)
    schedules = Schedule.objects.filter(trip=trip.id, deleted_at=None).order_by(
        "date", "start_time"
    )
    grouped_schedules = {}
    # 根據行程的日期屬性將行程分組並提取日期
    for date, group in groupby(schedules, key=attrgetter("date")):
        grouped_schedules[date] = list(group)
    # 獲取行程的日期範圍
    date_range = Schedule.get_date_range(trip)
    member_ids = TripMember.objects.filter(trip_id=id).order_by('id').values_list('member_id', flat=True)
    members = Member.objects.filter(id__in=member_ids)
    return render(request, "schedules/index.html", {"schedule_dates": grouped_schedules, "date_range": date_range, "trip": trip, "members": members})


def new(request, id):
    trip = get_object_or_404(Trip, pk=id)
    start_date = timezone.localtime(trip.start_date)
    end_date = timezone.localtime(trip.end_date)
    date_range = Schedule.get_date_range(trip)
    return render(
        request, "schedules/new.html", {"trip": trip, "date_range": date_range}
    )


def new_member(request, id):
    trip = get_object_or_404(Trip, pk=id)
    return render(request, "schedules/new_member.html", {"trip": trip})


@require_POST
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


@require_POST
def create_member(request, id):
    trip = get_object_or_404(Trip, id=id)
    email = request.POST["email"]
    is_editable = (request.POST['editable'] == 'True')
    member = get_object_or_404(Member, email=email)
    TripMember.objects.create(trip=trip, member=member, editable=is_editable)
    trip.number += 1
    trip.save()
    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


def show(request, id):
    schedules = get_object_or_404(Schedule, pk=id)
    trip = schedules.trip
    if request.method == "POST":
        schedules.date = request.POST["date"]
        schedules.spot_name = request.POST["spot_name"]
        schedules.start_time = request.POST["start_time"]
        schedules.end_time = request.POST["end_time"]
        schedules.note = request.POST["note"]
        schedules.save()
        return redirect("schedules:show", id=id)
    else:
        return render(
            request, "schedules/show.html", {"schedules": schedules, "trip": trip}
        )


def update(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    start_date = timezone.localtime(schedule.trip.start_date)
    end_date = timezone.localtime(schedule.trip.end_date)
    date_range = Schedule.get_date_range(schedule.trip)
    return render(
        request,
        "schedules/update.html",
        {"schedule": schedule, "date_range": date_range},
    )


@require_POST
def delete(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    schedule.deleted_at = timezone.now()
    schedule.save()
    return redirect("trips:schedules:index", id=schedule.trip_id)


@require_POST
def delete_member(request, id1, id2):
    trip_member = get_object_or_404(TripMember, trip_id=id1, member_id=id2)
    trip_member.delete()
    trip = get_object_or_404(Trip, pk=id1)
    trip.number -= 1
    trip.save()
    return redirect("trips:schedules:index", id=id1)
