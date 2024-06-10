from django.urls import path, include
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.home, name="index"),
    path("new", views.new, name="new"),
    path("map", views.map, name="map"),
    path("add", views.create, name="add"),
    path("<id>/update/", views.update, name="update"),
    path("<id>/delete/", views.delete, name="delete"),
    path("<id>/schedules/", include("schedules.urls")),
    path("<id>/new-member", views.new_member, name="new-member"),
    path("<id>/add-member", views.create_member, name="add-member"),
    path(
        "<trip_id>/<member_id>/delete-member", views.delete_member, name="delete-member"
    ),
    path("<trip_id>/<member_id>/delete-self", views.delete_self, name="delete-self"),
    path("<id>/add-member/edit/confirm", views.edit_confirm, name="edit-confirm"),
    path("<id>/add-member/edit", views.new_member_edit, name="add-member-edit"),
    path("<id>/add-member/watch", views.new_member_watch, name="add-member-watch"),
]
