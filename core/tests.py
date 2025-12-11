from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class HealthCheckTests(APITestCase):
    def test_health_endpoint_returns_ok(self):
        url = reverse('health-check')  # from core/urls.py name='health-check'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "ok")
        self.assertIn("HelpingHand backend is running",
                      response.data.get("message", ""))
