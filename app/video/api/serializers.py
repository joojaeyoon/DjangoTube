from rest_framework import serializers

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        exclude = ["description", "video_link", "updated_at"]


class VideoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = "__all__"
