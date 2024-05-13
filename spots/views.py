from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView
from .models import Spot
from .form import SpotForm
from django.urls import reverse_lazy

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
