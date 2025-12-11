from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer


class DonationListCreateView(generics.ListCreateAPIView):

    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show donations of the logged-in user
        return Donation.objects.filter(donor=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Save with logged-in user as donor
        donation = serializer.save(donor=self.request.user)

        # Simple update of campaign current_amount
        campaign = donation.campaign
        campaign.current_amount += donation.amount
        campaign.save()
