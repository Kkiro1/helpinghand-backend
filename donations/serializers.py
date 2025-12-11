from rest_framework import serializers
from .models import Donation


class DonationSerializer(serializers.ModelSerializer):
    donor = serializers.ReadOnlyField(source='donor.username')
    campaign_title = serializers.ReadOnlyField(source='campaign.title')

    class Meta:
        model = Donation
        fields = [
            'id',
            'campaign',
            'campaign_title',
            'donor',
            'amount',
            'created_at',
        ]
        read_only_fields = ['id', 'donor', 'campaign_title', 'created_at']
