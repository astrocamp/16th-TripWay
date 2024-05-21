from django.db import models

# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=255, null=True, unique=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    phone = models.CharField(max_length=20, null=True)
    url = models.URLField(max_length=255, null=True)
    rating = models.FloatField(null=True)
    place_id = models.CharField(max_length=255, null=True)

    # city = models.CharField(max_length=100, default="")
    # description = models.TextField(default="")
    # MondayHr = models.CharField(max_length=50)
    # TuesdayHr = models.CharField(max_length=50)
    # WednesdayHr = models.CharField(max_length=50)
    # ThursdayHr = models.CharField(max_length=50)
    # FridayHr = models.CharField(max_length=50)
    # SaturdayHr = models.CharField(max_length=50)
    # SundayHr = models.CharField(max_length=50)
    # PhotoReference1 = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # CommentTimes = models.CharField(max_length=50)
    # SpotType = models.CharField(max_length=255)
    # FavTimes = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    def clean(self):
        # 檢查 rating 是否為有效值，若為 'N/A' 則將其設置為 None
        if self.rating == "N/A":
            self.rating = None
