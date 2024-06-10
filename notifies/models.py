from django.db import models
from members.models import Member
from trips.models import Trip

class Notification(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message