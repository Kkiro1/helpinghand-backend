from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Campaign

User = get_user_model()


class CampaignTests(APITestCase):
    def setUp(self):
        self.list_url = reverse('campaign-list-create')

        self.user = User.objects.create_user(
            username='campaign_owner',
            email='owner@example.com',
            password='StrongPass123!'
        )

        self.campaign_data = {
            "title": "Help Family X",
            "description": "Raising money for medical bills.",
            "goal_amount": "10000.00",
            "start_date": "2025-01-01",
            "end_date": "2025-02-01",
            "is_active": True,
        }

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_list_campaigns_empty(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_campaign_authenticated(self):
        self.authenticate()
        response = self.client.post(
            self.list_url, self.campaign_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Campaign.objects.first().title,
                         self.campaign_data["title"])

    def test_cannot_create_campaign_unauthenticated(self):
        response = self.client.post(
            self.list_url, self.campaign_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
