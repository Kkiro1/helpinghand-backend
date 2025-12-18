from rest_framework import generics, permissions
from django.db.models import Q

from .models import Campaign
from .serializers import CampaignSerializer


class CampaignListCreateView(generics.ListCreateAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Campaign.objects.all().order_by('-created_at')
        search = (self.request.query_params.get('search') or '').strip()
        category = (self.request.query_params.get('category') or '').strip()

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category and category.lower() != 'all':
            qs = qs.filter(category__iexact=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
