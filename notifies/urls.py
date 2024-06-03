from django.urls import path
from . import views

app_name = "notifies"

urlpatterns = [
    path("", views.notification_list, name='notification_list'),
    path("delete/<int:notification_id>/", views.delete_notification, name="delete_notification"),
    path("mark_as_read/<int:notification_id>/", views.mark_as_read, name="mark_as_read"),
]