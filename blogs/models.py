from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django_ckeditor_5.fields import CKEditor5Field

class BlogsMediaStorage(S3Boto3Storage):
    location = "blogs"
    file_overwrite = False

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = CKEditor5Field("Text", config_name="extends")
    image = models.ImageField(upload_to="blogs/", storage=BlogsMediaStorage())

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"