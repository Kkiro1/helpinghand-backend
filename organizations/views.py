from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import OrgCampaign, OrgDonation
from .serializers import OrgCampaignSerializer, OrgDonationSerializer, OrgProfileSerializer
from .permissions import IsOrganizationUser


class OrgCampaignListCreateView(generics.ListCreateAPIView):
    serializer_class = OrgCampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationUser]

    def get_queryset(self):
        return OrgCampaign.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrgCampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrgCampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationUser]

    def get_queryset(self):
        return OrgCampaign.objects.filter(owner=self.request.user)


class OrgDonationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrgDonationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationUser]

    def get_queryset(self):
        return OrgDonation.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrgDonationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrgDonationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationUser]

    def get_queryset(self):
        return OrgDonation.objects.filter(owner=self.request.user)


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated, IsOrganizationUser])
def org_profile_view(request):
    if request.method == 'GET':
        serializer = OrgProfileSerializer(instance=request.user)
        return Response(serializer.data)

    serializer = OrgProfileSerializer(instance=request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(OrgProfileSerializer(instance=request.user).data)
