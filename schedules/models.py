from django.db import models
from django.utils import timezone
from members.models import Members

class Schedules(models.Model):
    members = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)



# members/1/schedule/1/spots/index.html