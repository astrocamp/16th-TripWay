from django.db import models
from spots.models import Spot
from members.models import Member
class Comment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE) 
    spot = models.ForeignKey(Spot, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    value = models.IntegerField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at} - Rating: {self.value}"
