from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from members.models import MemberSpot
from trips.models import TripMember
from .form import SpotForm
from .models import Spot


class IndexView(ListView):
    model = Spot

    # 執行身份驗證，檢查使用者是否已登入
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class ShowView(DetailView):
    model = Spot

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk):
        spot = self.get_object()
        return redirect("spots:show", pk=spot.id)


class CreateView(CreateView):
    model = Spot
    template_name = "spots/create.html"
    form_class = SpotForm
    success_url = reverse_lazy("spots:index")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


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
