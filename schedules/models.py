from django.db import models

class Schedules(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # TRANSPORT_CHOICES = [
    #     ('walk', '走路'),
    #     ('public', '大眾運輸'),
    #     ('car', '汽車'),
    #     ('motorcycle', '機車'),
    # ]
    transportation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)