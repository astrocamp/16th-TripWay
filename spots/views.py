from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from datetime import timedelta

from trips.models import Trip, TripMember
from members.models import MemberSpot
from schedules.models import Schedule
from .models import Spot
from .form import SpotForm


class IndexView(ListView):
    model = Spot


class ShowView(DetailView):
    model = Spot

    def post(self, request, pk):
        spot = self.get_object()
        return redirect("spots:show", pk=spot.id)


class CreateView(CreateView):
    model = Spot
    template_name = "spots/create.html"
    form_class = SpotForm
    success_url = reverse_lazy("spots:index")


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


def search(request):
    spots = Spot.objects.all()
    return render(request, "spots/search.html", {"spots": spots})


def my_view(request):
    show_footer = False
    return render(request, "spots/search.html", {"show_footer": show_footer})


@csrf_exempt
def save_spot(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        phone = request.POST.get("phone")
        url = request.POST.get("url")
        rating = request.POST.get("rating")
        place_id = request.POST.get("place_id")

        rating = float(rating) if rating and rating != "N/A" else None

        if not place_id:
            return JsonResponse(
                {"status": "error", "message": "place_id is required"}, status=400
            )

        spot, created = Spot.objects.get_or_create(
            place_id=place_id,
            defaults={
                "name": name,
                "address": address,
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
                "phone": phone,
                "url": url,
                "rating": rating,
            },
        )

        if not created:
            spot.name = name
            spot.address = address
            spot.city = city
            spot.latitude = latitude
            spot.longitude = longitude
            spot.phone = phone
            spot.url = url
            spot.rating = rating
            spot.save()

        return JsonResponse(
            {"status": "success", "message": "Spot saved successfully!"}
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=400
    )


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
