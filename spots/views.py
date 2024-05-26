from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from members.models import MemberSpot
from trips.models import TripMember
from .form import SpotForm
from .models import Spot, LoginRequired


class IndexView(LoginRequired, ListView):
    model = Spot


class ShowView(LoginRequired, DetailView):
    model = Spot
    
    def post(self, request, pk):
        spot = self.get_object()
        return redirect("spots:show", pk=spot.id)


class CreateView(LoginRequired,CreateView):
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
    member = request.user
    spot = get_object_or_404(Spot, id=pk)
    
    if request.method == "GET":
        is_favorite = MemberSpot.objects.filter(member=member, spot=spot).exists()
        return JsonResponse({"is_favorite": is_favorite})
    
    elif request.method == "POST":
        is_favorite = MemberSpot.objects.filter(member=member, spot=spot).exists()
        
        if is_favorite:
            MemberSpot.objects.filter(member=member, spot=spot).delete()
            return JsonResponse({"status": "removed"})
        else:
            MemberSpot.objects.create(member=member, spot=spot)
            return JsonResponse({"status": "added"})