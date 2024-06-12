from django.db import models
from django.contrib.auth.models import AbstractUser
from spots.models import Spot


class Member(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    level = models.CharField(max_length=10, default="基本會員")
    image = models.ImageField(null=True, blank=True)


class MemberSpot(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="members")
    spot = models.ForeignKey(
        Spot, on_delete=models.CASCADE, related_name="favorite_spots"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("member", "spot")
