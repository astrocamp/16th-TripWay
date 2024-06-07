from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

ADMIN = os.getenv("ADMIN_URL")
urlpatterns = [
    path("", views.home, name="home"),
    path(f"{ ADMIN }/", admin.site.urls),
    path("members/", include("django.contrib.auth.urls")),
    path("members/", include("members.urls")),
    path("members/upgrade/", include("payments.urls")),
    path("trips/", include("trips.urls")),
    path("schedules/", include("schedules.urls")),
    path("accounts/", include("allauth.urls")),
    path("spots/", include("spots.urls")),
    path("notifications/", include("notifies.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
