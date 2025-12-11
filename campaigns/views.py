from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Campaign
from .serializers import CampaignSerializer


class CampaignListCreateView(generics.ListCreateAPIView):
    """
    GET /api/campaigns/    → list campaigns
    POST /api/campaigns/   → create new campaign (authenticated)
    """
    queryset = Campaign.objects.all().order_by('-created_at')
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Set the owner to the logged-in user
        serializer.save(owner=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/campaigns/<id>/       → campaign details
    PUT/PATCH /api/campaigns/<id>/ → update
    DELETE /api/campaigns/<id>/    → delete
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
