from django.db import models

class Schedules(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default="")
    end_date = models.DateTimeField(default="")
    # TRANSPORT_CHOICES = [
    #     ('walk', '走路'),
    #     ('public', '大眾運輸'),
    #     ('car', '汽車'),
    #     ('motorcycle', '機車'),
    # ]
    transportation = models.CharField(max_length=20)