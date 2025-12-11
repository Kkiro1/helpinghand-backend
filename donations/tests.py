from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from campaigns.models import Campaign
from .models import Donation

User = get_user_model()


class DonationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='donor_user',
            email='donor@example.com',
            password='StrongPass123!'
        )

        self.campaign = Campaign.objects.create(
            title='Test Campaign',
            description='Test description',
            goal_amount='1000.00',
            current_amount='0.00',
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
            owner=self.user,
        )

        self.url = reverse('donation-list-create')

        self.donation_data = {
            "campaign": self.campaign.id,
            "amount": "200.00",
        }

    def test_cannot_donate_when_unauthenticated(self):
        response = self.client.post(
            self.url, self.donation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Donation.objects.count(), 0)

    def test_create_donation_updates_campaign_amount(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url, self.donation_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donation.objects.count(), 1)

        self.campaign.refresh_from_db()
        self.assertEqual(str(self.campaign.current_amount), "200.00")
