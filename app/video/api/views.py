from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from video.models import Comment, Video

from .pagination import CommentPagination, VideoPagination
from .serializers import (CommentSerializer, VideoDetailSerializer,
                          VideoSerializer)


class VideoUploadAPIView(views.APIView):
    """ 비디오 파일 업로드 API """
    pass


class VideoListAPIView(generics.ListAPIView):
    """ 비디오 리스트 API """

    queryset = Video.objects.order_by("-created_at")
    serializer_class = VideoSerializer
    pagination_class = VideoPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    """ 비디오 디테일 API """

    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_object(self):
        """ 비디오 조회시 조회수 ++ """
        video = super().get_object()
        video.view_count = video.view_count+1

        video.save()

        return video


class CommentListAPIView(generics.ListAPIView):
    """ 댓글 리스트 API """

    queryset = Comment.objects.order_by("created_at")
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        self.queryset = Comment.objects.filter(
            video=kwargs.get("pk")).order_by("created_at")
        return super().list(request, *args, **kwargs)
