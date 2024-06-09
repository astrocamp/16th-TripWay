import os
from decimal import Decimal
import requests
from django.core.management.base import BaseCommand
from spots.models import Spot
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "填寫 spot 初始資料"

    def handle(self, *args, **options):
        print("正在執行你的腳本...")
        api_key = os.getenv("GOOGLE_API_KEY")
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        query = "熱門景點"
        parameters = {
            "query": query,
            "language": "zh-TW",
            "key": api_key,
            "location": "23.6978,120.9605",
            "radius": "100000",
        }
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            data = response.json()["results"]
        else:
            print("無法從 Google API 獲取數據")
            return

        place_details_url = "https://maps.googleapis.com/maps/api/place/details/json"

        for place in data:
            place_id = place.get("place_id")
            if place_id:
                details_response = requests.get(
                    place_details_url,
                    params={"place_id": place_id, "key": api_key, "language": "zh-TW"},
                )
                if details_response.status_code == 200:
                    details_data = details_response.json().get("result", {})
                else:
                    print(f"無法獲取 place_id 為 {place_id} 的詳細數據")
                    continue

                city = None
                for component in place.get("address_components", []):
                    if "administrative_area_level_1" in component["types"]:
                        city = component["long_name"]
                        break

                Spot.objects.get_or_create(
                    name=place["name"],
                    defaults={
                        "address": place.get("formatted_address", None),
                        "city": (
                            city
                            or str(place["formatted_address"]).split("台灣")[1][0:3]
                            if "台灣" in place["formatted_address"]
                            else None
                        ),
                        "latitude": Decimal(str(place["geometry"]["location"]["lat"])),
                        "longitude": Decimal(str(place["geometry"]["location"]["lng"])),
                        "phone": details_data.get("formatted_phone_number", None),
                        "url": details_data.get("website", None),
                        "rating": place.get("rating", None),
                        "place_id": place_id,
                        "opening_hours": (
                            " ".join(
                                details_data.get("opening_hours", {}).get(
                                    "weekday_text", []
                                )
                            )
                            if details_data.get("opening_hours")
                            else None
                        ),
                        "description": details_data.get("editorial_summary", {}).get(
                            "overview", None
                        ),
                        "photo_url": (
                            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={details_data['photos'][0]['width']}&photoreference={details_data['photos'][0]['photo_reference']}&key={api_key}"
                            if "photos" in details_data
                            and len(details_data["photos"]) > 0
                            else None
                        ),
                    },
                )
        print("腳本執行完畢")
