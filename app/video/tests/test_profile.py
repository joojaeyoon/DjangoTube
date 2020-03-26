from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from video.models import Profile

from django.urls import reverse
from django.contrib.auth.models import User


class TestProfile(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")

        self.profile = Profile.objects.filter(user=self.user)[0]

        self.token = Token.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile(self):
        """ 프로필 디테일 GET 테스트 """

        url = reverse("api:profile-detail")

        payload = {
            "token": self.token,
        }

        res = self.client.get(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("user"), self.user.username)

    def test_subscribe_user(self):
        """ 구독 테스트 """

        user2 = User.objects.create_user(username="user2", password="password")

        url = reverse("api:profile-detail")

        payload = {
            "token": self.token,
            "subscribe": user2.username
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsubscribe_user(self):
        """ 구독 취소 테스트 """

        user2 = User.objects.create_user(username="user2", password="password")
        user2_profile = Profile.objects.filter(user=user2)[0]

        self.profile.subscribed.add(user2)
        user2_profile.subscriber.add(self.user)

        url = reverse("api:profile-detail")

        payload = {
            "token": self.token,
            "unsubscribe": user2.username
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
