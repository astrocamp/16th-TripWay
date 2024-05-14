from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Trip
from members.models import Member

# 列出目前行程
def home(request):
    trips = Trip.objects.all().order_by(
        "start_date"
    )
    member = request.user
    trips = [trip for trip in trips if member in trip.member.all()]
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
    trip = Trip(
        name=request.POST["name"],
        start_date=request.POST["start_date"],
        end_date=request.POST["end_date"],
        transportation=request.POST["transportation"],
    )
    trip.save()
    
    member = request.user
    trip.member.add(member)

    return redirect("trips:index")


# 刪除行程(硬刪)
@require_POST
def delete(request, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.delete()
    return redirect("trips:index")
