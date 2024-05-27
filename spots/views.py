import re
import googlemaps
from hanziconv import HanziConv

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, View
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


class SearchView(View):
    def get(self, request):
        query = request.GET.get("q")

        if not query:
            return JsonResponse({"error": "沒有提供搜索關鍵詞"}, status=400)

        spot = Spot.objects.filter(name__icontains=query).first()

        if spot:
            return JsonResponse({"redirect_url": spot.get_absolute_url()})
        else:
            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            places_result = gmaps.places(query=query, language="zh-TW")

            if places_result["results"]:
                top_result = places_result["results"][0]
                name = HanziConv.toTraditional(top_result["name"]).replace("颱", "台")
                address = HanziConv.toTraditional(
                    top_result.get("formatted_address", "")
                ).replace("颱", "台")
                location = top_result["geometry"]["location"]
                place_id = top_result["place_id"]
                city = extract_city(address)
                phone = top_result.get("formatted_phone_number")
                url = top_result.get("url")
                rating = top_result.get("rating")

                spot, created = Spot.objects.get_or_create(
                    name=name,
                    defaults={
                        "address": address,
                        "city": city,
                        "latitude": location["lat"],
                        "longitude": location["lng"],
                        "phone": phone,
                        "url": url,
                        "rating": rating,
                        "place_id": place_id,
                    },
                )

                result = {
                    "名稱": spot.name,
                    "地址": spot.address,
                    "城市": spot.city,
                    "緯度": spot.latitude,
                    "經度": spot.longitude,
                    "電話": spot.phone,
                    "網址": spot.url,
                    "評分": spot.rating,
                    "地點ID": spot.place_id,
                    "重定向鏈接": spot.get_absolute_url(),
                }
                return JsonResponse(result)
            else:
                return JsonResponse({"error": "未找到結果"}, status=404)


def extract_city(address):
    match = re.search(r"台灣(.+?)[市縣區]", address)
    if match:
        city = match.group(1)
        return city.strip()
    else:
        return None


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
