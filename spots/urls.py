from django.urls import path
from .views import (
    ShowView,
    IndexView,
    CreateView,
    toggle_favorite,
    add_schedule,
)

app_name = "spots"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new", CreateView.as_view(), name="new"),
    path("<int:pk>/show", ShowView.as_view(), name="show"),
    path("<int:pk>/show/add", add_schedule, name="add_schedule"),
    path("<int:pk>/toggle_favorite", toggle_favorite, name="toggle_favorite"),
]
