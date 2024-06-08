from django.db import models
from django.utils import timezone
from members.models import Member
from datetime import timedelta
from PIL import Image
from io import BytesIO


class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)
    owner = models.IntegerField(default=0)
    number = models.IntegerField(default=1)
    image = models.ImageField(null=True, default=None)
    upload_date = models.DateField(default=timezone.now)

    def get_date_range(self):
        return [
            self.start_date + timedelta(days=x) 
            for x in range((self.end_date - self.start_date).days + 1)
        ]
    
    def compress_image(image):
        img = Image.open(image)
        img.thumbnail((200, 200))
        output = BytesIO()
        img.save(output, format="PNG", quality=70)
        output.seek(0)
        return output

class TripMember(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_editable = models.BooleanField(default=True)
