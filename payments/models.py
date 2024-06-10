from django.db import models
from members.models import Member

# Create your models here.


class Payment(models.Model):
    order = models.CharField(max_length=255)
    price = models.FloatField()
    trade_no = models.CharField(max_length=255, null=True, default=None)
    status = models.CharField(max_length=255, null=True, default="PENDING")
    paid_at = models.CharField(max_length=255, null=True, default=None)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
