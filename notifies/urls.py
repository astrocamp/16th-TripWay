# notifies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notify_list, name='notify_list'),
    path("mark_as_read/<int:notification_id>/", views.mark_as_read, name="mark_as_read"),
]
