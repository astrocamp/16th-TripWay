from django.core.management.base import BaseCommand
from spots.models import Spot 
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = "填寫spot初始資料"

    def handle(self, *args, **options):
        self.stdout.write("正在執行你的腳本...")
        
        # Google Places API 金鑰
        api_key = os.getenv("API_KEY") 

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

        for place in data:  
            Spot.objects.get_or_create(
                name = place["name"],
                defaults={
                    "address": place["formatted_address"],
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "phone": place.get("formatted_phone_number", "N/A"),
                    "url": place.get("website", "N/A"),
                    "rating": place["rating"],
                }
            )
            
        self.stdout.write("腳本執行完畢")



