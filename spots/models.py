from django.db import models
from schedules.models import Schedules
from django.utils import timezone

class SpotsList(models.Model):
    schedule = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    spot_name = models.CharField(max_length=100)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now) 
    note = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.spot_name