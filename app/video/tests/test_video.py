from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from video.models import Comment, Video


class TestUnAuthorizedVideo(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.video = Video.objects.create(
            author=self.user,
            title="test title",
            description="test description",
            video_link="media/test.mp4")

    def test_get_videos(self):
        """ 비디오 리스트 API 테스트 """
        url = reverse("api:video-list")

        res = self.client.get(url)

        data = res.data.get("results")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('title'), self.video.title)
        self.assertIsNone(data[0].get("description"))

    def test_get_video_detail(self):
        """ 비디오 디테일 API 테스트 """
        url = reverse("api:video-detail", kwargs={"pk": self.video.id})

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data.get("description"))

    def test_video_view_count(self):
        """ 비디오 조회수 확인 테스트 """

        url = reverse("api:video-detail", kwargs={"pk": self.video.id})

        res = self.client.get(url)

        prev_count = res.data.get("view_count")

        res = self.client.get(url)

        count = res.data.get("view_count")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(prev_count+1, count)


class TestAuthorizedVideo(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")

        self.token = Token.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_create_video(self):
        """ 비디오 생성 API 테스트 """

        url = reverse("api:video-create")

        payload = {
            "token": self.token,
            "title": "test video",
            "video_link": "1.mp4"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("title"), payload["title"])

    def test_create_invalid_video(self):
        """ 유효하지 않은 비디오 생성 테스트 """

        url = reverse("api:video-create")

        payload = {
            "token": self.token,
            "video_link": "test.mp4"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
