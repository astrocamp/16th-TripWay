from django.urls import path
from .views import ShowView, IndexView, CreateView, toggle_favorite, add_schedule

app_name = "spots"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new", CreateView.as_view(), name="new"),
    path("<int:pk>/show", ShowView.as_view(), name="show"),
    path("<int:pk>/show/add", add, name="add"),
    path("search/", views.search, name="search"),
    path("save_spot/", views.save_spot, name="save_spot"),
    path("delete/<str:spot_id>/", views.delete, name="delete"),
    path("<int:pk>/toggle_favorite", toggle_favorite, name="toggle_favorite"),
]
