from rest_framework import status
from rest_framework.test import APITestCase
from video.models import Video, Comment

from django.urls import reverse
from django.contrib.auth.models import User


class TestComment(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1", password="password")

        self.video = Video.objects.create(
            author=self.user,
            title="test title",
            video_link="media/test.mp4"
        )

        self.comment = Comment.objects.create(
            author=self.user,
            video=self.video,
            text="comment test"
        )

    def test_get_comments(self):
        """ 특정 동영상 댓글 조회 테스트 """

        url = reverse("api:comment-list", kwargs={"pk", self.video.id})

        res = self.client.get(url)

        data = res.data.get("results")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get("text"), self.comment.text)
