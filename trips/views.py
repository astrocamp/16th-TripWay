from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings
from .models import Trip, TripMember
from members.models import Member
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Trip
from django.conf import settings
from django.contrib import messages


@login_required
def home(request):
    if request.method == "POST":
        trip_id = request.POST.get("trip_id")
        trip = get_object_or_404(Trip, id=trip_id)

        trip.name = request.POST["name"]
        trip.start_date = request.POST["start_date"]
        trip.end_date = request.POST["end_date"]
        trip.transportation = request.POST["transportation"]
        if "image" in request.FILES:
            trip.image = request.FILES["image"]

        trip.save()
        return redirect("trips:index")

    else:
        member = request.user
        trip_members = TripMember.objects.filter(member=member)
        trip_ids = trip_members.values_list("trip_id", flat=True)
        trips = Trip.objects.filter(id__in=trip_ids).order_by("start_date")
        trips = [{"t": trip, "tm": trip_members.get(trip=trip)} for trip in trips]
        return render(request, "trips/index.html", {"trips": trips})


@login_required
def new(request):
    return render(request, "trips/new.html")


@login_required
def new_member(request, id):
    trip = get_object_or_404(Trip, pk=id)
    return render(request, "trips/new_member.html", {"trip": trip})


# google map
@login_required
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
        image = request.FILES["image"]

        if end_date < start_date:
            messages.error(request, "結束日期不能早於開始日期")
            return redirect("trips:new")

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
        messages.success(request, "旅程創建成功！")
        return redirect("trips:index")


@login_required
def update(request, id):
    trips = get_object_or_404(Trip, pk=id)
    return render(request, "trips/update.html", {"trips": trips})


@require_POST
@login_required
def create_member(request, id):
    trip = get_object_or_404(Trip, id=id)
    email = request.POST["email"]
    is_editable = request.POST["is_editable"] == "True"
    member = get_object_or_404(Member, email=email)
    TripMember.objects.create(trip=trip, member=member, is_editable=is_editable)
    trip.number += 1
    trip.save()
    return redirect(reverse("trips:schedules:index", kwargs={"id": trip.id}))


@require_POST
@login_required
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
@login_required
def delete_member(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    return redirect("trips:schedules:index", id=trip_id)


@require_POST
@login_required
def delete_self(request, trip_id, member_id):
    delete_TripMember(trip_id, member_id)
    return redirect("trips:index")
