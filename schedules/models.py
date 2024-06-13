from django.db import models
from trips.models import Trip
from django.utils import timezone
from spots.models import Spot


class Schedule(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    spot = models.ForeignKey(
        Spot,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    date = models.DateField(default=timezone.now)
    spot_name = models.CharField(max_length=100)
    start_time = models.TimeField(default=timezone.now, null=True)
    end_time = models.TimeField(default=timezone.now, null=True)
    note = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    order = models.PositiveIntegerField(default=0) 

    def save(self, *args, **kwargs):
        if self.order == 0:  # 如果 order 為預設值
            max_order = Schedule.objects.filter(trip=self.trip).aggregate(models.Max('order'))['order__max']
            if max_order is None:
                max_order = 0
            self.order = max_order + 1
        super(Schedule, self).save(*args, **kwargs)


    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.spot_name

    @property
    def spot_latitude(self):
        return self.spot.latitude if self.spot else None

    @property
    def spot_longitude(self):
        return self.spot.longitude if self.spot else None


    class Meta:
        ordering = ["order", "date", "start_time"]  # 按 order 排序
