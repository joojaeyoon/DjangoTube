from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


class Video(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    video_link = models.FilePathField(path=settings.MEDIA_ROOT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title, allow_unicode=True)

        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Comment(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
