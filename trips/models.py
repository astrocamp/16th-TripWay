from django.db import models
from django.utils import timezone
from members.models import Member

class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)
    owner = models.IntegerField(default=0)
    number = models.IntegerField(default=1)
    trips_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name 


class TripMember(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_editable = models.BooleanField(default=True)
    
    

class Photo(models.Model):
    image = models.ImageField(blank=False, null=False,  upload_to="trips_coverPhoto/")
    upload_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.image.url
