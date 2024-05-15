from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from .models import Spot
from .form import SpotForm
from django.urls import reverse_lazy
from trips.models import Trip
from datetime import timedelta

# Create your views here.


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


def add(request, pk):
    member = request.user
    trips = member.trips.all()
    spot = get_object_or_404(Spot, pk=pk)

    trips_dates = []
    for trip in trips:
        date_range = [
            (trip.start_date + timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range((trip.end_date - trip.start_date).days + 1)
        ]
        trips_dates.append({"trip": trip, "date_range": date_range})
    context = {"spot": spot, "trips": trips, "trips_dates": trips_dates}
    return render(request, "spots/add.html", context)
