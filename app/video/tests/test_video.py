from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from video.models import Comment, Video


class TestVideo(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.video = Video.objects.create(
            author=self.user,
            title="test title",
            description="test description",
            video_link="test/link")

    def test_get_videos(self):
        url = reverse("api:video-list")

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0].get('title'), self.video.title)
        self.assertIsNone(res.data[0].get("description"))

    def test_get_video_detail(self):
        url = reverse("api:video-detail", kwargs={"pk": self.video.id})

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data.get("description"))
        self.assertEqual(res.data.get("slug"),
                         self.video.title.replace(" ", "-"))
