from rest_framework import serializers

from video.models import Video, Comment


class VideoSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()

    class Meta:
        model = Video
        exclude = ["description", "video_link", "updated_at"]


class VideoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(CommentCreateSerializer):

    author = serializers.StringRelatedField()
