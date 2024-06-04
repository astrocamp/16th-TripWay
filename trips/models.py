from django.db import models
from django.utils import timezone
from members.models import Member
from datetime import timedelta
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)
    owner = models.IntegerField(default=0)
    number = models.IntegerField(default=1)
    image = models.ImageField(
        null=True, default=None,  upload_to="trips_coverPhoto/"
    )
    upload_date = models.DateField(default=timezone.now)

    def get_date_range(self):
        return [self.start_date + timedelta(days=x) for x in range((self.end_date - self.start_date).days + 1)]
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            max_size = (600, 600)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()
            img_format = "PNG" if img.mode == "RGBA" else "JPEG"
            img.save(thumb_io, format=img_format)
            thumb_io.seek(0)
            file_extension = "png" if img.mode == "RGBA" else "jpg"
            new_file_name = f"{self.image.name.split('.')[0]}_thumb.{file_extension}" 
            self.image.save(new_file_name, ContentFile(thumb_io.read()), save=False)
        super().save(*args, **kwargs)



class TripMember(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_editable = models.BooleanField(default=True)
