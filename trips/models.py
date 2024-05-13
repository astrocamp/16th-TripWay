from django.db import models
from django.utils import timezone
from members.models import Member


class Trip(models.Model):
    member = models.ManyToManyField(Members)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    transportation = models.CharField(max_length=20)

    def __str__(self):
        return self.spot_name
