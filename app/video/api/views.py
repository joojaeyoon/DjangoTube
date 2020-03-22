from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from video.models import Comment, Video

from .pagination import CommentPagination, VideoPagination
from .serializers import (CommentSerializer, VideoDetailSerializer,
                          VideoSerializer)

import uuid


class VideoUploadAPIView(views.APIView):
    """ 비디오 파일 업로드 API """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):

        upload_file = request.data["video"]

        filename = str(upload_file).split(".")
        ext = filename[-1]

        if ext not in ["mp4", "avi"]:
            return JsonResponse({"error": "BAD REQUEST"}, status=400)

        filename = ".".join(filename[:-1])
        filename = filename+"-"+str(uuid.uuid4())+"."+ext

        destination = open(settings.MEDIA_ROOT+f"/videos/{filename}", "wb+")

        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()

        response = {"data": "Some data"}

        return JsonResponse(response, status=200)


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
