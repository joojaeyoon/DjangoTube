from django.urls import path

from .views import VideoListCreateAPIView, VideoRetrieveAPIView, CommentListAPIView, VideoUploadAPIView, CommentCreateAPIView, ProfileRetrieveAPIView

app_name = "api"

urlpatterns = [
    path("videos/", VideoListCreateAPIView.as_view(), name="video-list"),
    path("videos/<pk>", VideoRetrieveAPIView.as_view(), name="video-detail"),
    path("videos/<pk>/comment", CommentCreateAPIView.as_view(),
         name="comment-create"),
    path("videos/<pk>/comments", CommentListAPIView.as_view(), name="comment-list"),
    path("video/upload", VideoUploadAPIView.as_view(), name="upload-video"),
    path("profile",
         ProfileRetrieveAPIView.as_view(), name="profile-detail")
]
