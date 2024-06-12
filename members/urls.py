from django.urls import path, include
from . import views
from spots.views import toggle_favorite

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("spots/<spot_id>/favorite/", toggle_favorite, name="favorite"),
    path("profile/", views.profile, name="profile"),
    path("create", views.create, name="create"),
]
