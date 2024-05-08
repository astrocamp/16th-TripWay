from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.home, name="index"), # 行程首頁
    path("new", views.new, name="new"), # 輸入行程資料的頁面
    path("add", views.create, name="add"), # 寫入資料庫的觸發按鈕
    # path("<id>/edit", views.edit, name="edit"), # 未做
    # path("<id>/delete", views.delete, name="delete"), # 未做
    # path("<id>", views.show, name="show") # 連到 spots
]