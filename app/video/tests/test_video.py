from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from video.models import Comment, Video


class TestVideo(APITestCase):

    def setUp(self):
        self.url = reverse("api:video-list")

    def test_get_videos(self):
        res = self.client.get(self.url)
