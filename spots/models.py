from django.db import models

# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=255, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=20, null=True)
    url = models.URLField(max_length=255, null=True)
    rating = models.FloatField(max_length=5, null=True)
