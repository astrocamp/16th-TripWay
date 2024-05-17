from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("members/", include("django.contrib.auth.urls")),
    path("members/", include("members.urls")),
    path("trips/", include("trips.urls")),
    path("schedules/", include("schedules.urls")),
    path("accounts/", include("allauth.urls")),
    path("spots/", include("spots.urls")),
    path("members/upgrade/", include("payments.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
