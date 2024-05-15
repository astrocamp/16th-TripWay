from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Trip, TripMember
from members.models import Member

# 列出目前行程
def home(request):
    member = request.user
    trip_ids = TripMember.objects.filter(member_id=member.id).values_list('trip_id', flat=True)
    trips = Trip.objects.filter(id__in=trip_ids).order_by(
        "start_date"
    )
    return render(request, "trips/index.html", {"trips": trips})


# 輸入行程資訊
def new(request):
    return render(request, "trips/new.html")


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
    TripMember.objects.create(trip=trip, member=member, editable=True)
    
    return redirect("trips:index")


# 刪除行程(硬刪)
@require_POST
def delete(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.delete()
    return redirect("trips:index")
