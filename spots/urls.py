from django.urls import path
from .views import (
    ShowView,
    IndexView,
    CreateView,
    DeleteSpotView,
    toggle_favorite,
    add_schedule,
    search,
    save_spot,
    delete_spot,
)

app_name = "spots"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new", CreateView.as_view(), name="new"),
    path("<int:pk>/show", ShowView.as_view(), name="show"),
    path("delete/<int:pk>", DeleteSpotView.as_view(), name="delete_spot_list"),
    path("<int:pk>/show/add", add_schedule, name="add_schedule"),
    path("search/", search, name="search"),
    path("save_spot/", save_spot, name="save_spot"),
    path("delete_spot/<str:spot_id>/", delete_spot, name="delete_spot"),
    path("<int:pk>/toggle_favorite", toggle_favorite, name="toggle_favorite"),
]
