from django.shortcuts import render, redirect, get_object_or_404 # 渲染轉址和判斷有沒有資料
from django.views.decorators.http import require_POST # 判斷是不是 POST
from .models import Schedules # 從同家的 model 取 class


# 列出行程
def home(req):
    schedules = Schedules.objects.all()
    return render(req, "schedules/index.html", {"schedules":schedules})

# 新增行程
def new(req):
    return render(req, "schedules/new.html")

# 寫入資料庫
@require_POST
def create(req):
    schedule = Schedules(
        name=req.POST["name"],
        start_date=req.POST["start_date"],
        end_date=req.POST["end_date"],
        transportation=req.POST["transportation"] 
    )
    schedule.save()
        
    return redirect("schedules:index")

# 刪除資料
@require_POST    
def delete(req, id):
    schedule = get_object_or_404(Schedules, pk=id)
    schedule.delete()
    return redirect('schedules:index')