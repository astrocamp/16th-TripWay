from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.index, name="index"),
    path("article/<int:blog_id>/", views.article, name="article"),
    path("new/", views.new, name="new"),
    path("edit/<int:blog_id>/", views.edit, name="edit"),
    path("delete/<int:blog_id>/", views.delete_blog, name="delete"),
]
