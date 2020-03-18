from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import generics

from video.models import Video

from .serializers import VideoDetailSerializer, VideoSerializer


class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
