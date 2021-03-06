from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

from app.utils import generate_random_string, get_video_data


class Video(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="videos")

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    video_link = models.FilePathField(path=settings.MEDIA_ROOT+"/videos")
    thumbnail = models.ImageField(blank=True)

    time = models.CharField(max_length=12, blank=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.thumbnail == "":
            self.slug = slugify(self.title, allow_unicode=True) + \
                "-"+generate_random_string()
            self.time, thumbnail_path = get_video_data(
                self.video_link, self.slug)
            self.thumbnail = thumbnail_path
            self.video_link = "/"+"/".join(self.video_link.split("/")[2:])
            self.thumbnail = "/"+"/".join(thumbnail_path.split("/")[-2:])

        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
