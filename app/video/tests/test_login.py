from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestLogin(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")

    def test_login_valid_account(self):
        """ 로그인 테스트 """

        url = "/rest-auth/login/"

        payload = {
            "username": "testuser",
            "password": "password"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data.get("key"))

    def test_login_invalid_account(self):
        """ 유효하지 않은 계정 로그인 테스트 """

        url = "/rest-auth/login/"

        payload = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_account(self):
        """ 계정 생성 테스트 """

        url = "/rest-auth/registration/"

        payload = {
            "username": "testuser2",
            "email": "test@test.com",
            "password1": "supersecretpassword",
            "password2": "supersecretpassword"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data.get("key"))

    def test_create_invalid_account(self):
        """ 유효하지 않은 계정 생성 테스트 """

        url = "/rest-auth/registration/"

        payload = {
            "username": "testuser3",
            "email": "test2@test.com",
            "password1": "supersecretpassword",
            "password2": "othersecretpassword"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
