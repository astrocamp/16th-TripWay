from django.db import models

# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    MondayHr = models.CharField(max_length=50)
    TuesdayHr = models.CharField(max_length=50)
    WednesdayHr = models.CharField(max_length=50)
    ThursdayHr = models.CharField(max_length=50)
    FridayHr = models.CharField(max_length=50)
    SaturdayHr = models.CharField(max_length=50)
    SundayHr = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    PhotoReference1 = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField()
    SpotType = models.CharField(max_length=255)
