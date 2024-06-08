from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class BlogsMediaStorage(S3Boto3Storage):
    location = "blogs"
    file_overwrite = False

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blogs/", storage=BlogsMediaStorage())

    def __str__(self):
        return self.title
