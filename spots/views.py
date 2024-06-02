import re
import googlemaps
from hanziconv import HanziConv

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

class IndexView(LoginRequired, ListView):
    model = Spot

class ShowView(LoginRequired, DetailView):
    model = Spot
    template_name = 'spot_detail.html'  # 指定模板文件名
    context_object_name = 'spot'

    def post(self, request, pk):
        spot = self.get_object()

        # 處理評論邏輯
        if 'comment' in request.POST and 'rating' in request.POST:
            comment_content = request.POST.get('comment')
            rating_value = request.POST.get('rating')

            if comment_content and rating_value != '0':
                Comment.objects.create(content=comment_content, spot=spot, user=request.user, value=int(rating_value))
                messages.success(request, "已提交留言！")
                
                # 更新景點的平均評分
                comments = Comment.objects.filter(spot=spot)
                total_comments = comments.count()
                average_rating = comments.aggregate(Avg('value'))['value__avg']
                spot.rating = average_rating
                spot.save()
            else:
                messages.error(request, "請先完成評分！")
            return redirect('spots:show', pk=spot.id)

        if 'edit_comment_id' in request.POST:
            comment_id = request.POST['edit_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            comment_content = request.POST.get('edit_comment_content')
            if comment_content:
                comment.content = comment_content
                comment.save()
                messages.success(request, "留言已修改！")
            return redirect('spots:show', pk=spot.id)

        if 'delete_comment_id' in request.POST:
            comment_id = request.POST['delete_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            messages.success(request, "留言已刪除！")
            
            # 更新景點的平均評分
            comments = Comment.objects.filter(spot=spot)
            total_comments = comments.count()
            average_rating = comments.aggregate(Avg('value'))['value__avg'] if total_comments > 0 else 0
            spot.rating = average_rating
            spot.save()
            
            return redirect('spots:show', pk=spot.id)

        return redirect("spots:show", pk=spot.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.get_object()
        user = self.request.user

        # 確認當前用戶是否喜愛該景點
        member_spot = MemberSpot.objects.filter(spot=spot, member=user).exists()

        # 添加評論表單和評論數據到上下文
        comments = Comment.objects.filter(spot=spot)
        total_comments = comments.count()
        average_rating = comments.aggregate(Avg('value'))['value__avg'] if total_comments > 0 else 0
        form = CommentForm()
        alert = self.request.session.pop('alert', None)
        context.update({
            'comments': comments,
            'form': form,
            'alert': alert,
            'average_rating': average_rating,
            'total_comments': total_comments,
            'member_spot': member_spot,
        })

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
                name = (
                    HanziConv.toTraditional(top_result["name"])
                    .replace("颱", "台")
                    .replace("傢", "家")
                )
                address = (
                    HanziConv.toTraditional(top_result.get("formatted_address", ""))
                    .replace("颱", "台")
                    .replace("傢", "家")
                )
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
