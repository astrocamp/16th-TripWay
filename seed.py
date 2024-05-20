from django.core.management.base import BaseCommand
from spots.models import Spot 
import requests


# 定義函數以獲取地點詳細資訊
def get_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,geometry,rating,website,opening_hours",
        "key": api_key,
        "language": "zh-TW",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["result"] if data.get("status") == "OK" else None


# API 金鑰
api_key = "AIzaSyCZzfaT30wnP7RD1eUtvA1U3K-fCLn4O4w"  # Google Places API 金鑰


# 請求 URL
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"


# 準備請求參數
query = "熱門景點"  # 查詢關鍵字（根據需要更改）
parameters = {
    "query": query,
    "language": "zh-TW",
    "key": api_key,
}

# 發送 GET 請求
response = requests.get(url, params=parameters)

if response.status_code == 200:
    data = response.json()
    data = data["results"]


for place in data:  # 生成 100 条假数据
    Spot.objects.create(
        name = place["name"],
        latitude = place["geometry"]["location"]["lat"],
        longitude = place["geometry"]["location"]["lng"],
        city = place["formatted_address"],
        rating = place["rating"],
        phone = place["formatted_phone_number"],
        url = place["website"]
    )

