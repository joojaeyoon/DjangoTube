import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from video.models import Comment, Video

from .pagination import CommentPagination, VideoPagination
from .serializers import (CommentCreateSerializer, CommentSerializer,
                          VideoDetailSerializer, VideoSerializer)


class VideoUploadAPIView(views.APIView):
    """ 비디오 파일 업로드 API """

    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):

        upload_file = request.data["video"]

        content_type = upload_file.content_type.split("/")[0]

        if content_type != "video":
            return JsonResponse({"error": "invalid content type."}, status=400)
        if upload_file.size > 41943040:  # 40 MB 초과
            return JsonResponse({"error": "The uploaded file is larger than the limited size."}, status=400)

        filename = upload_file.name.split(".")
        ext = filename[-1]

        filename = ".".join(filename[:-1])
        filename = filename+"-"+str(uuid.uuid4())+"."+ext

        destination = open(settings.MEDIA_ROOT+f"/videos/{filename}", "wb+")

        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()

        response = {"filepath": filename}

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


class CommentCreateAPIView(generics.CreateAPIView):
    """ 댓글 작성 API """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        video_id = kwargs.get("pk")
        token = request.data.get("token")

        user = Token.objects.filter(key=token)[0].user

        data = request.data.copy()

        data["video"] = video_id
        data["author"] = user.id
        data.pop("token")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data)

        return Response(serializer.data, status=201, headers=headers)
