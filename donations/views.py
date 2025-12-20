from decimal import Decimal

from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer


class DonationListCreateView(generics.ListCreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user)

        campaign = donation.campaign
        campaign.current_amount = (campaign.current_amount or Decimal('0')) + donation.amount
        campaign.save(update_fields=['current_amount'])
