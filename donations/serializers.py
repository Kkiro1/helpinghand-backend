from rest_framework import serializers

from campaigns.models import Campaign
from .models import Donation


class DonationSerializer(serializers.ModelSerializer):
    campaignId = serializers.IntegerField(write_only=True, required=False)

    campaignTitle = serializers.ReadOnlyField(source='campaign.title')
    organization = serializers.SerializerMethodField()
    date = serializers.ReadOnlyField(source='created_at')

    # IMPORTANT: float output so DonationHistory reduce() works
    amount = serializers.FloatField()

    paymentMethod = serializers.CharField(source='payment_method', required=False)
    isAnonymous = serializers.BooleanField(source='is_anonymous', required=False)

    donor = serializers.ReadOnlyField(source='donor.username')

    class Meta:
        model = Donation
        fields = [
            'id',
            'campaignTitle',
            'organization',
            'amount',
            'date',
            'paymentMethod',
            'isAnonymous',
            'status',
            'campaign',
            'campaignId',
            'donor',
            'created_at',
        ]
        read_only_fields = ['id', 'donor', 'created_at', 'campaignTitle', 'date', 'organization']

    def validate(self, attrs):
        if 'campaign' not in attrs and 'campaignId' in attrs:
            campaign_id = attrs.pop('campaignId')
            try:
                attrs['campaign'] = Campaign.objects.get(pk=campaign_id)
            except Campaign.DoesNotExist:
                raise serializers.ValidationError({'campaignId': 'Invalid campaign id.'})
        return attrs

    def get_organization(self, obj) -> str:
        owner = obj.campaign.owner
        profile = getattr(owner, 'profile', None)
        if profile and getattr(profile, 'ui_name', None):
            return profile.ui_name
        return owner.username
