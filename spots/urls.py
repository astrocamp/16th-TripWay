from django.urls import path, include
from .views import ShowView, IndexView, CreateView

app_name = "spots"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new", CreateView.as_view(), name="new"),
    path("<int:pk>/show", ShowView.as_view(), name="show"),
]
