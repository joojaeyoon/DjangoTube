from django.urls import path

from .views import VideoListAPIView, VideoRetrieveAPIView, CommentListAPIView, VideoUploadAPIView, CommentCreateAPIView

app_name = "api"

urlpatterns = [
    path("videos/", VideoListAPIView.as_view(), name="video-list"),
    path("videos/<pk>", VideoRetrieveAPIView.as_view(), name="video-detail"),
    path("videos/<pk>/comment", CommentCreateAPIView.as_view(),
         name="comment-create"),
    path("videos/<pk>/comments", CommentListAPIView.as_view(), name="comment-list"),
    path("video/upload", VideoUploadAPIView.as_view(), name="upload-video"),
]
