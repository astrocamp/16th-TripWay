from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Member(AbstractUser):
    email = models.EmailField(max_length=255, 
    unique=True)


class MemberSpot(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="members"
    )
    spot = models.ForeignKey("Spot", on_delete=models.CASCADE, related_name='favorite_spots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        unique_together = ('member', 'spot')