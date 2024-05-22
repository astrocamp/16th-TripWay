from django.urls import path, include
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.home, name="index"),  # 行程列表
    path("new", views.new, name="new"),  # 輸入行程資料的頁面
    path("map", views.map, name="map"),  # 地圖頁面
    path("add", views.create, name="add"),  # 寫入資料庫的觸發按鈕
    path("delete/<id>/", views.delete, name="delete"),  # 刪除行程
    path("<id>/schedules/", include("schedules.urls")),  # 連到 schedules:index
    path("<id>/new-member", views.new_member, name="new-member"),
    path("<id>/add-member", views.create_member, name="add-member"),
    path("<trip_id>/<member_id>/delete-member", views.delete_member, name="delete-member"),
    path("<trip_id>/<member_id>/delete-self", views.delete_self, name="delete-self"),
    path("upload_photo", views.upload_photo, name="upload_photo"),
    path("delete_photo", views.delete_photo, name="delete_photo"), 
]
