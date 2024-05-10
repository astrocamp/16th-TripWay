from django.urls import path, include
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.home, name="index"),  # 行程列表
    path("new", views.new, name="new"),  # 輸入行程資料的頁面
    path("add", views.create, name="add"),  # 寫入資料庫的觸發按鈕
    path("delete/<id>/", views.delete, name="delete"),  # 刪除行程
    path("<id>/schedules/", include("schedules.urls")),  # 連到 schedules:index
]