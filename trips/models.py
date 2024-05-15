from django.db import models
from django.utils import timezone
from members.models import Member


class Trip(models.Model):
    member = models.ManyToManyField(Member, related_name="trips")
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)
    owner = models.IntegerField(default=0)
    number = models.IntegerField(default=1)

    # def __str__(self):
    #     return self.spot_name


class TripMember(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    editable = models.BooleanField(default=True)
    
