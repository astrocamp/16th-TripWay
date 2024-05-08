from django.db import models

class spots_list(models.Model):
    spot_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField() 
    note = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)