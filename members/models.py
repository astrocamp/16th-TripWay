from django.db import models
from django.contrib.auth.models import AbstractUser
from spots.models import Spot


class Member(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)


class MemberSpot(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="members"
    )
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="favorite_spots")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("member", "spot")