from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Member(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
