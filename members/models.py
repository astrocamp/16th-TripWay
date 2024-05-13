from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Members(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)

class MemberSpot(models.Model):
    """
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='members')
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='spots')
    """
    pass

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()