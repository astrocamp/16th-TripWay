from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Spot(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=255, null=True, unique=True)
    city = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    phone = models.CharField(max_length=20, null=True)
    url = models.URLField(max_length=255, null=True)
    rating = models.FloatField(
        null=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    place_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.rating == "N/A":
            self.rating = None
