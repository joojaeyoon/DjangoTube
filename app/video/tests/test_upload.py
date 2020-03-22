from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestUploadVideUnAuthorized(APITestCase):

    def setUp(self):
        self.file = open("media/test.mp4", "rb")
        self.url = reverse("api:upload-video")

    def test_unauthorized_user_upload_video(self):
        """ 로그인 하지않고 비디오 업로드 API 테스트 """

        payload = {
            "video": self.file
        }

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUploadAuthorized(APITestCase):

    def setUp(self):
        self.file = open("media/test.mp4", "rb")
        self.user = User.objects.create_user("testuser", "supersecret")
        self.url = reverse("api:upload-video")

        self.client.force_authenticate(self.user)

    def test_upload_video(self):
        """ 비디오 업로드 테스트 """

        payload = {
            "video": self.file
        }

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_upload_invalid_video(self):
        """ 유효하지 않은 비디오 업로드 테스트 """

        file = open("media/test.txt", "r")

        payload = {
            "video": file
        }

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
