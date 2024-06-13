from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.create, name="add"),
    path("add_day", views.add_day, name="add_day"),
    path("delete_day", views.delete_day, name="delete_day"),
    path("get_schedule/", views.get_schedule, name="get_schedule"),
    path("<id>/update", views.update, name="update"),
    path("<id>/delete", views.delete, name="delete"),
    path("<id>/show", views.show, name="show"),
    path("update_schedule_order", views.update_schedule_order, name="update_schedule_order"),
]
