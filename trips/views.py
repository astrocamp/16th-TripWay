from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Trip


# 列出目前行程
def home(req):
    trips = Trip.objects.all()
    return render(req, "trips/index.html", {"trips": trips})


# 輸入行程資訊
def new(req):
    return render(req, "trips/new.html")


# 寫入資料庫
@require_POST
def create(req):
    trip = Trip(
        name=req.POST["name"],
        start_date=req.POST["start_date"],
        end_date=req.POST["end_date"],
        transportation=req.POST["transportation"],
    )
    trip.save()

    return redirect("trips:index")


# 刪除行程(硬刪)
@require_POST
def delete(req, id):
    trip = get_object_or_404(Trip, pk=id)
    trip.delete()
    return redirect("trips:index")