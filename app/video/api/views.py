from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import generics

from video.models import Video

from .serializers import VideoDetailSerializer, VideoSerializer
from .pagination import VideoPagination


class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.order_by("-created_at")
    serializer_class = VideoSerializer
    pagination_class = VideoPagination


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer

    def get_object(self):
        """ 비디오 조회시 조회수 ++ """
        video = super().get_object()
        video.view_count = video.view_count+1

        video.save()

        return video
