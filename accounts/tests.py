from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')   # from accounts/urls.py
        self.login_url = reverse('login')
        self.me_url = reverse('me')

        self.user_data = {
            "username": "nardeen_test",
            "email": "nardeen@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "nardeen",
            "last_name": "raafat",
        }

    def test_register_creates_user(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]
                         ["username"], self.user_data["username"])

    def test_login_returns_tokens(self):
        # First register the user
        self.client.post(self.register_url, self.user_data, format='json')

        # Then login
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_me_returns_current_user(self):
        # Register
        self.client.post(self.register_url, self.user_data, format='json')

        # Login to get access token
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        login_response = self.client.post(
            self.login_url, login_data, format='json')
        access = login_response.data["tokens"]["access"]

        # Call /me with Authorization header
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure "user" key exists
        self.assertIn("user", response.data)
        # Compare username inside "user" object
        self.assertEqual(response.data["user"]
                         ["username"], self.user_data["username"])
