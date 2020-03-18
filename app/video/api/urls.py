from django.urls import path

from .views import VideoListAPIView, VideoRetrieveAPIView

app_name = "api"

urlpatterns = [
    path("videos/", VideoListAPIView.as_view(), name="video-list"),
    path("videos/<pk>", VideoRetrieveAPIView.as_view(), name="video-detail")
]
