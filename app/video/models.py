from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

from app.utils import generate_random_string
import cv2


def get_video_data(filepath):
    video = cv2.VideoCapture(filepath)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)

    video.set(cv2.CAP_PROP_POS_FRAMES, int(frame_count/2))

    _, frame = video.read()

    cv2.imwrite(filepath+"-thumbnail.png", frame)

    video.release()

    duration = frame_count/fps

    minutes = int(duration/60)
    seconds = int(duration % 60)

    time = f'{minutes}:{seconds}'

    return time


class Video(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    video_link = models.FilePathField(path=settings.MEDIA_ROOT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(blank=True)
    time = models.CharField(max_length=12, blank=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title, allow_unicode=True) + \
            "-"+generate_random_string()
        self.time = get_video_data(self.video_link)
        self.video_link = "/"+"/".join(self.video_link.split("/")[2:])
        self.thumbnail = f"{self.video_link}-thumbnail.png"

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
