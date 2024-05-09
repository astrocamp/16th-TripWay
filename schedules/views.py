<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Schedules
=======
from django.shortcuts import render, redirect  # 渲染和轉址
from django.views.decorators.http import require_POST  # 判斷是不是 POST
from .models import Schedules  # 從同家的 model 取 class
>>>>>>> 87549ca (Issue#18 update)


# 列出目前行程
def home(req):
    return render(req, "schedules/index.html", {"schedules": schedules})


# 輸入行程資訊
def new(req):
    return render(req, "schedules/new.html")

<<<<<<< HEAD
# 新增行程(寫入資料庫)
=======

# 寫入資料庫
>>>>>>> 87549ca (Issue#18 update)
@require_POST
def create(req):
    schedule = Schedules(
        name=req.POST["name"],
        start_date=req.POST["start_date"],
        end_date=req.POST["end_date"],
        transportation=req.POST["transportation"],
    )
    schedule.save()
<<<<<<< HEAD
        
    return redirect("schedules:index")

# 刪除行程(硬刪)
@require_POST    
def delete(req, id):
    schedule = get_object_or_404(Schedules, pk=id)
    schedule.delete()
    return redirect('schedules:index')
=======

    return redirect("root")
>>>>>>> 87549ca (Issue#18 update)
