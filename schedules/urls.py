from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("new-member", views.new_member, name="new-member"),
    path("add", views.create, name="add"),
    path("<id>/update", views.update, name="update"),
    path("<id>/delete", views.delete, name="delete"),
    path("<id>/show", views.show, name="show"),
]
