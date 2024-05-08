from django.db import models

# Create your models here.


class Members(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
