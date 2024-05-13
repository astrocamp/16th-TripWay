from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Schedule
from trips.models import Trip
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta

def index(request, id):
    trip = get_object_or_404(Trip, pk=id)
    schedules = Schedule.objects.filter(trip=trip.id, deleted_at=None).order_by(
        "date", "start_time"
    )
    return render(
        request, "schedules/index.html", {"schedules": schedules, "trip": trip}
    )


def new(request, id):
    trip = get_object_or_404(Trip, pk=id)
    start_date = trip.start_date
    end_date = trip.end_date
    date_range = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range((end_date - start_date).days + 1)]
    return render(request, "schedules/new.html", {"trip": trip, "date_range": date_range})


@require_POST
def create(request, id):
    trip = get_object_or_404(Trip, id=id)

    schedules = Schedule(
        date=request.POST["date"],
        spot_name=request.POST["spot_name"],
        start_time=request.POST["start_time"],
        end_time=request.POST["end_time"],
        note=request.POST["note"],
        trip=trip,
    )

    schedules.save()

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
    start_date = schedule.trip.start_date
    end_date = schedule.trip.end_date
    date_range = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range((end_date - start_date).days + 1)]
    return render(request, "schedules/update.html", {"schedule": schedule, "date_range": date_range})


@require_POST
def delete(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    schedule.deleted_at = timezone.now()
    schedule.save()
    return redirect("trips:schedules:index", id=schedule.trip_id)
