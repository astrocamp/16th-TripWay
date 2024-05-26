from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import timedelta

from members.models import MemberSpot
from trips.models import Trip, TripMember
from schedules.models import Schedule
from .form import SpotForm
from .models import Spot, LoginRequired


class IndexView(LoginRequired, ListView):
    model = Spot


class ShowView(LoginRequired, DetailView):
    model = Spot

    def post(self, request, pk):
        spot = self.get_object()
        return redirect("spots:show", pk=spot.id)


class CreateView(LoginRequired, CreateView):
    model = Spot
    template_name = "spots/create.html"
    form_class = SpotForm
    success_url = reverse_lazy("spots:index")


@login_required
def add_schedule(request, pk):
    member = request.user
    trips_member = TripMember.objects.filter(member=member)
    trips = [trip_member.trip for trip_member in trips_member]
    spot = get_object_or_404(Spot, pk=pk)

    trips_dates = []
    for trip in trips:
        date_range = trip.get_date_range()
        trips_dates.append({"trip": trip, "date_range": date_range})
    context = {"spot": spot, "trips": trips, "trips_dates": trips_dates}
    return render(request, "spots/add.html", context)


@csrf_exempt
@login_required
def toggle_favorite(request, pk):
    if request.method == "POST":
        member = request.user
        spot = get_object_or_404(Spot, id=pk)

        try:
            member_spot = MemberSpot.objects.get(member=member, spot=spot)
            member_spot.delete()
            is_favorite = False
        except MemberSpot.DoesNotExist:
            MemberSpot.objects.create(member=member, spot=spot)
            is_favorite = True

        return JsonResponse({"is_favorite": is_favorite})
    else:
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def delete(request, spot_id):
    if request.method == "DELETE":
        spot = get_object_or_404(Spot, place_id=spot_id)
        spot.delete()
        return JsonResponse(
            {"status": "success", "message": "Spot deleted successfully!"}
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=400
    )
