from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Trip, TripMember
from members.models import Member

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


# 寫入資料庫
@require_POST
def create(request):
    member = request.user
    trip = Trip(
        name=request.POST["name"],
        start_date=request.POST["start_date"],
        end_date=request.POST["end_date"],
        transportation=request.POST["transportation"],
        owner = member.id
    )
    trip.save()
    TripMember.objects.create(trip=trip, member=member, is_editable=True)
    
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
