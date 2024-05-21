from django.core.management.base import BaseCommand
from spots.models import Spot 
import requests

class Command(BaseCommand):
    help = "填寫spot初始資料"

    def handle(self, *args, **options):
        self.stdout.write('正在執行你的腳本...')
        # 你的腳本邏輯
        
        # Google Places API 金鑰
        api_key = "AIzaSyCZzfaT30wnP7RD1eUtvA1U3K-fCLn4O4w"  


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
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "city": place["formatted_address"],
                    "description": place["rating"],
                    # "rating": place["rating"],
                    # "phone": place["formatted_phone_number"],
                    # "url": place["website"]
                }
                
                
            )
            
        self.stdout.write('腳本執行完畢')



