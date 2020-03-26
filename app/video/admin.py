from django.contrib import admin

from .models import Video, Comment, Profile

admin.site.register(Video)
admin.site.register(Comment)

admin.site.register(Profile)
