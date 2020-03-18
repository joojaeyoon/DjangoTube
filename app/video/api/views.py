from rest_framework import generics
from .serializers import VideoSerializer
from video.models import Video


class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
