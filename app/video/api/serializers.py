from rest_framework import serializers

from video.models import Video, Comment, Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    # subscriber = serializers.StringRelatedField(many=True)
    # subscribed = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = "__all__"
