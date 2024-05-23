from django.core.management.base import BaseCommand
from spots.models import Spot
from decimal import Decimal
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "填寫spot初始資料"

    def handle(self, *args, **options):
        self.stdout.write("正在執行你的腳本...")
        api_key = os.getenv("API_KEY")
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        query = "熱門景點"
        parameters = {
            "query": query,
            "language": "zh-TW",
            "key": api_key,
        }
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            data = response.json()["results"]

        for place in data:
            city = None
            for component in place.get("address_components", []):
                if "administrative_area_level_1" in component["types"]:
                    city = component["long_name"]
                    break

            Spot.objects.get_or_create(
                name=place["name"],
                defaults={
                    "address": place.get("formatted_address", None),
                    "city": str(place["formatted_address"]).split("台灣")[1][0:3],
                    "latitude": Decimal(str(place["geometry"]["location"]["lat"])),
                    "longitude": Decimal(str(place["geometry"]["location"]["lng"])),
                    "phone": place.get("formatted_phone_number", None),
                    "url": place.get("website", None),
                    "rating": place.get("rating", None),
                    "place_id": place.get("place_id", None),
                },
            )
        self.stdout.write("腳本執行完畢")
