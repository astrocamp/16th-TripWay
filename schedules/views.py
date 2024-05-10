from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Schedules
from spots.models import spots_list


# 列出目前行程
def home(req):
    return render(req, "schedules/index.html", {"schedules": schedules})


# 輸入行程資訊
def new(req):
    return render(req, "schedules/new.html")


# 寫入資料庫
@require_POST
def create(req):
    schedule = Schedules(
        name=req.POST["name"],
        start_date=req.POST["start_date"],
        end_date=req.POST["end_date"],
        transportation=req.POST["transportation"],
    )
    schedule.save()

    return redirect("schedules:index")


# 刪除行程(硬刪)
@require_POST
def delete(req, id):
    schedule = get_object_or_404(Schedules, pk=id)
    schedule.delete()
    return redirect("schedules:index")
