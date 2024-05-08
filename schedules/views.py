from django.shortcuts import render, redirect # 渲染和轉址
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