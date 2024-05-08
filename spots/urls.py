from django.urls import path
from . import views

app_name="Spot"

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("add", views.create, name="add"),
    path("<id>/update", views.update, name="update"),
    path("<id>delete", views.delete, name="delete"),
    path("<id>", views.show, name="show")
]