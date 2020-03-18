from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from video.models import Comment, Video


class TestVideo(APITestCase):

    def setUp(self):
        self.url = reverse("api:video-list")
        Video.objects.create(title="test_title", video_link="test/link")

    def test_get_videos(self):
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'test_title')
