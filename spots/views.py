import re
import googlemaps
from hanziconv import HanziConv
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .form import SpotForm
from .models import Spot, LoginRequired
from comments.models import Comment
from comments.forms import CommentForm
from members.models import MemberSpot
from trips.models import Trip, TripMember
from schedules.models import Schedule


class IndexView(ListView):
    model = Spot
    template_name = "spots/spot_list.html"
    context_object_name = "spots"

    def get_queryset(self):
        sort_option = self.request.GET.get("sort", "rating_desc")
        queryset = Spot.objects.all()
        for spot in queryset:
            comments = Comment.objects.filter(spot=spot)
            average_rating = comments.aggregate(Avg("value"))["value__avg"] or 0
            spot.average_rating = average_rating
            spot.total_comments = comments.count()
        if sort_option == "average_rating_desc":
            queryset = sorted(queryset, key=lambda x: x.average_rating, reverse=True)
        elif sort_option == "comment_count_desc":
            queryset = sorted(queryset, key=lambda x: x.total_comments, reverse=True)
        else:
            queryset = sorted(queryset, key=lambda x: x.rating or 0.0, reverse=True)

        return queryset


class ShowView(DetailView):
    model = Spot
    template_name = "spots/spot_detail.html"
    context_object_name = "spot"

    def get_place_details(self, place_id):
        google_api_key = settings.GOOGLE_API_KEY
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=website,formatted_address,formatted_phone_number,opening_hours,reviews&key={google_api_key}&language=zh-TW"

        response = requests.get(details_url)
        details = response.json()

        if "result" in details:
            result = details["result"]
            website = result.get("website", "N/A")
            address = result.get("formatted_address", "N/A")
            phone_number = result.get("formatted_phone_number", "N/A")
            opening_hours = result.get("opening_hours", {}).get("weekday_text", [])
            about = result.get("about", "N/A")
            return {
                "website": website,
                "address": address,
                "phone_number": phone_number,
                "opening_hours": opening_hours,
                "about": about,
            }
        return {}

    def post(self, request, pk):
        spot = self.get_object()
        if self.request.user.is_authenticated:
            if "comment" in request.POST and "rating" in request.POST:
                comment_content = request.POST.get("comment")
                rating_value = request.POST.get("rating")

                if comment_content and rating_value != "0":
                    Comment.objects.create(
                        content=comment_content,
                        spot=spot,
                        user=request.user,
                        value=int(rating_value),
                    )
                    messages.success(request, "已提交留言！")
                    comments = Comment.objects.filter(spot=spot).select_related('user')
                    total_comments = comments.count()
                    average_rating = comments.aggregate(Avg("value"))["value__avg"]
                    spot.rating = average_rating
                    spot.save()
                else:
                    messages.error(request, "請先完成評分！")
                return redirect("spots:show", pk=spot.id)

            if "edit_comment_id" in request.POST:
                comment_id = request.POST["edit_comment_id"]
                comment = get_object_or_404(Comment, id=comment_id)
                comment_content = request.POST.get("edit_comment_content")
                if comment_content:
                    comment.content = comment_content
                    comment.save()
                    messages.success(request, "留言已修改！")
                return redirect("spots:show", pk=spot.id)

            if "delete_comment_id" in request.POST:
                comment_id = request.POST["delete_comment_id"]
                comment = get_object_or_404(Comment, id=comment_id)
                comment.delete()
                messages.success(request, "留言已刪除！")
                comments = Comment.objects.filter(spot=spot)
                total_comments = comments.count()
                average_rating = (
                    comments.aggregate(Avg("value"))["value__avg"]
                    if total_comments > 0
                    else 0
                )
                spot.rating = average_rating
                spot.save()

                return redirect("spots:show", pk=spot.id)

        return redirect("spots:show", pk=spot.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.get_object()
        comments = Comment.objects.filter(spot=spot).order_by('-created_at')

        user_comment = None
        if self.request.user.is_authenticated:
            user = self.request.user
            user_comment = comments.filter(user=user).first()

        total_comments = comments.count()
        average_rating = (
            comments.aggregate(Avg("value"))["value__avg"] if total_comments > 0 else 0
        )
        form = CommentForm()
        alert = self.request.session.pop("alert", None)
        place_id = spot.place_id
        place_details = self.get_place_details(place_id)

        if self.request.user.is_authenticated:
            member_spot = MemberSpot.objects.filter(spot=spot, member=self.request.user).exists()
            user_comment_exists = user_comment is not None
            context.update(
                {
                    "member_spot": member_spot,
                    "user_comment_exists": user_comment_exists,
                    "user_comment": user_comment, 
                }
            )

        context.update(
            {
                "comments": comments,
                "form": form,
                "alert": alert,
                "average_rating": average_rating,
                "total_comments": total_comments,
                "website": place_details.get("website", "N/A"),
                "phone_number": place_details.get("phone_number", "N/A"),
                "opening_hours": place_details.get("opening_hours", []),
                "reviews": place_details.get("reviews", []),
            }
        )

        return context

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
                place_id = top_result["place_id"]

                place_details = gmaps.place(place_id=place_id, language="zh-TW")

                details = place_details.get("result", {})
                name = (
                    HanziConv.toTraditional(details.get("name", ""))
                    .replace("颱", "台")
                    .replace("傢", "家")
                )
                address = (
                    HanziConv.toTraditional(details.get("formatted_address", ""))
                    .replace("颱", "台")
                    .replace("傢", "家")
                )
                location = details["geometry"]["location"]
                city = extract_city(address)
                phone = details.get("formatted_phone_number")
                url = details.get("website")
                rating = details.get("rating")
                weekday_text = details.get("opening_hours", {}).get("weekday_text", [])
                description = details.get("editorial_summary", {}).get("overview", None)

                formatted_weekday_text = (
                    " ".join(weekday_text) if weekday_text else None
                )
                photo_url = (
                    f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={details['photos'][0]['width']}&photoreference={details['photos'][0]['photo_reference']}&key={settings.GOOGLE_API_KEY}"
                    if "photos" in details and len(details["photos"]) > 0
                    else None
                )
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
                        "opening_hours": formatted_weekday_text,
                        "description": description,
                        "photo_url": photo_url,
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
                    "營業時間": spot.opening_hours,
                    "描述": spot.description,
                    "營業時間文字": weekday_text,
                    "圖片URL": photo_url,
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
    trips_member = TripMember.objects.filter(member=member, is_editable=True)
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

    if request.method == "POST":
        is_favorite = MemberSpot.objects.filter(member=member, spot=spot).exists()

        if is_favorite:
            MemberSpot.objects.filter(member=member, spot=spot).delete()
            return JsonResponse({"status": "removed"})
        else:
            MemberSpot.objects.create(member=member, spot=spot)
            return JsonResponse({"status": "added"})