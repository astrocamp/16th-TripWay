from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.upgrade, name="upgrade"),
    path("create", views.create_order, name="create")

]
