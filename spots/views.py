from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from .models import Spot
from .form import SpotForm
from django.urls import reverse_lazy
from trips.models import Trip

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
    spot = get_object_or_404(Spot, pk=pk)
    trips = Trip.objects.all()
    context = {
        "spot": spot,
        "trips": trips,
    }
    return render(request, "spots/add.html", context)
