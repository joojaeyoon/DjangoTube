from django.urls import path

from .views import VideoListAPIView

app_name = "api"

urlpatterns = [
    path("videos/", VideoListAPIView.as_view(), name="video-list")
]
