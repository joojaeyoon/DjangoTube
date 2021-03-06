import uuid
import os

from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, views, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from video.models import Comment, Video

from .pagination import CommentPagination, VideoPagination
from .serializers import (CommentCreateSerializer, CommentListSerializer,
                          VideoDetailSerializer, VideoSerializer)


class VideoUploadAPIView(views.APIView):
    """ 비디오 파일 업로드 API """

    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):

        upload_file = request.data["video"]

        if request.FILES["video"]:
            upload_file = request.FILES["video"]

        content_type = upload_file.content_type.split("/")[0]

        if upload_file.size > 100*1024*1024:  # 100 MB 초과
            return JsonResponse({"error": "The uploaded file is larger than the limited size."}, status=400)

        filename = upload_file.name.split(".")
        ext = filename[-1]

        filename = ".".join(filename[:-1])
        filename = str(uuid.uuid4())+"."+ext

        destination = open(settings.MEDIA_ROOT+f"/videos/{filename}", "wb+")

        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()

        response = {"filepath": filename}

        return JsonResponse(response, status=200)


class VideoListCreateAPIView(generics.ListCreateAPIView):
    """ 비디오 리스트 API """

    queryset = Video.objects.order_by("-created_at")
    serializer_class = VideoSerializer
    pagination_class = VideoPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        token = request.data.get("token")

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = Token.objects.filter(key=token)[0].user

        data = request.data.copy()

        data["author"] = user.id
        data["video_link"] = os.path.join(
            settings.MEDIA_ROOT, "videos", data["video_link"])

        data.pop("token")

        self.serializer_class = VideoDetailSerializer

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data)

        serializer.data["author"] = user.username

        res = serializer.data.copy()

        res["author"] = user.username

        return Response(res, status=201, headers=headers)


class VideoRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
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

    def delete(self, request, *args, **kwargs):
        """ 비디오 삭제 """
        token = request.data.get("token")

        self.perform_authentication(request)

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = Token.objects.filter(key=token)[0].user
        video = Video.objects.filter(pk=kwargs.get("pk"))[0]

        if video.author == user:
            video.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """ 비디오 정보 업데이트 """
        token = request.data.get("token")

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = Token.objects.filter(key=token)[0].user
        video = Video.objects.filter(pk=kwargs.get("pk"))[0]

        if video.author == user:
            return super().patch(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(generics.ListAPIView):
    """ 댓글 리스트 API """

    queryset = Comment.objects.order_by("-created_at")
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        self.queryset = Comment.objects.filter(
            video=kwargs.get("pk")).order_by("-created_at")

        self.paginate_queryset(self.queryset)

        self.response = self.get_paginated_response(self.queryset)

        return super().list(request, *args, **kwargs)


class CommentCreateAPIView(generics.CreateAPIView):
    """ 댓글 작성 API """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        video_id = kwargs.get("pk")
        token = request.data.get("token")

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = Token.objects.filter(key=token)[0].user

        data = request.data.copy()

        data["video"] = video_id
        data["author"] = user.id
        data.pop("token")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data)

        serializer.data["author"] = user.username

        res = serializer.data.copy()

        res["author"] = user.username

        return Response(res, status=201, headers=headers)
