from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Schedule
from trips.models import Trip
from django.utils import timezone
from django.urls import reverse


def index(request, id):
    schedules = Schedule.objects.all().filter()
    # schedules = spots_list.objects.all().order_by("start_time")
    trip = get_object_or_404(Trip, pk=id)
    return render(
        request, "schedules/index.html", {"schedules": schedules, "trip": trip}
    )


def new(request, id):
    return render(request, "schedules/new.html")


@require_POST
def create(request, id):
    trip = get_object_or_404(Trip, id=id)

    schedules = Schedule(
        # date=request.POST["date"],
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
    schedules = get_object_or_404(Schedule, pk=id)
    return render(request, "schedules/update.html", {"schedules": schedules})


@require_POST
def delete(request, id):
    schedules = get_object_or_404(Schedule, pk=id)
    schedules.deleted_at = timezone.now()
    schedules.save()
    return redirect("schedules:index")
