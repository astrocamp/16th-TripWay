from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("", views.index, name="index"),  # 將路由設置為空字串
]
