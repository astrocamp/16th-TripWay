from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import SpotsList
from schedules.models import Schedules
from django.utils import timezone


@require_POST
def index(request, id):
    spots = SpotsList.objects.all().filter(schedule=id)
    # spots = spots_list.objects.all().order_by("start_time")
    schedule = get_object_or_404(Schedules, pk=id)
    return render(request, "spots/index.html", {"schedule": schedule, "spots": spots})


def new(request, id):
    return render(request, "spots/new.html")


@require_POST
def create(request):
    spots = SpotsList(
        # date=request.POST["date"],
        spot_name=request.POST["spot_name"],
        start_time=request.POST["start_time"],
        end_time=request.POST["end_time"],
        note=request.POST["note"],
    )
    spots.save()

    return redirect("spots:index")


def show(request, id):
    spots = get_object_or_404(SpotsList, pk=id)
    if request.method == "POST":
        spots.spot_name = request.POST["spot_name"]
        spots.start_time = request.POST["start_time"]
        spots.end_time = request.POST["end_time"]
        spots.note = request.POST["note"]
        spots.save()
        return redirect(f"/spots/{spots.id}")
    else:
        return render(request, "spots/show.html", {"spots": spots})


def update(request, id):
    spots = get_object_or_404(SpotsList, pk=id)
    return render(request, "spots/update.html", {"spots": spots})



@require_POST
def delete(request, id):
    spots = get_object_or_404(SpotsList, pk=id)
    spots.deleted_at = timezone.now()
    spots.save()
    return redirect("spots:index")
