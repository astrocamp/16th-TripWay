from django.urls import path, include
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.home, name="index"),  
    path("new", views.new, name="new"),  
    path("map", views.map, name="map"),  
    path("add", views.create, name="add"),  
    path("delete/<id>/", views.delete, name="delete"),  
    path("<id>/schedules/", include("schedules.urls")),  
    path("<id>/new-member", views.new_member, name="new-member"),
    path("<id>/add-member", views.create_member, name="add-member"),
    path("<trip_id>/<member_id>/delete-member", views.delete_member, name="delete-member"),
    path("<trip_id>/<member_id>/delete-self", views.delete_self, name="delete-self"),
    path("upload_photo", views.upload_photo, name="upload_photo"),
    path("delete_photo", views.delete_photo, name="delete_photo"), 
]
