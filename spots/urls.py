from django.urls import path
from .views import (
    ShowView,
    IndexView,
    CreateView,
    toggle_favorite,
    add_schedule,
    SearchView,
)

app_name = "spots"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new", CreateView.as_view(), name="new"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:pk>/show", ShowView.as_view(), name="show"),
    path("<int:pk>/show/add", add_schedule, name="add_schedule"),
    path("<int:pk>/favorite", toggle_favorite, name="favorite"),
]
