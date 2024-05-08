from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import spots_list


def index(request):
    spots=spots_list.objects.all().order_by("start_time")
    return render(request, "spots/index.html", {"spots":spots})


def new(request):
    return render(request, "spots/new.html")

@require_POST
def create(request):
    spots=spots_list(
        # date=request.POST["date"],
        spot_name=request.POST["spot_name"],
        start_time=request.POST["start_time"],
        end_time=request.POST["end_time"],
        note=request.POST["note"],
    )
    spots.save()

    return redirect("Spot:index")

def show(request, id):
    spots=get_object_or_404(spots_list, pk=id)
    if request.method == "POST":
        spots.spot_name=request.POST["spot_name"]
        spots.start_time=request.POST["start_time"]
        spots.end_time=request.POST["end_time"]
        spots.note=request.POST["note"]
        spots.save()
        return redirect(f"/spots/{spots.id}")
    else:
        return render(request, "spots/show.html", {"spots":spots})


def update(request, id):
    spots=get_object_or_404(spots_list, pk=id)
    return render(request, "spots/update.html", {"spots":spots})

@require_POST
def delete(request, id):
    spots=get_object_or_404(spots_list, pk=id)
    spots.delete()
    return redirect("Spot:index")