from django.db import models

# Create your models here.
class Schedules(models.Model):
    name = models.CharField(max_langth=100)
    start_date = models.DateTimeField(auto_now=True)
    ended_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="")