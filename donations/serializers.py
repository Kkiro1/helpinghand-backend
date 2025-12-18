from rest_framework import serializers
from decimal import Decimal

from campaigns.models import Campaign
from .models import Donation


class DonationSerializer(serializers.ModelSerializer):
    # Frontend sends campaignId
    campaignId = serializers.IntegerField(write_only=True, required=False)

    campaignTitle = serializers.ReadOnlyField(source='campaign.title')
    organization = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source='created_at', read_only=True)

    # Input as Decimal (safe), output will still be numeric
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

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
        read_only_fields = [
            'id', 'donor', 'created_at', 'campaignTitle', 'date', 'organization'
        ]

    def validate(self, attrs):
        if 'campaign' not in attrs and 'campaignId' in attrs:
            campaign_id = attrs.pop('campaignId')
            try:
                attrs['campaign'] = Campaign.objects.get(pk=campaign_id)
            except Campaign.DoesNotExist:
                raise serializers.ValidationError({'campaignId': 'Invalid campaign id.'})
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Guarantee JS gets a number (DonationHistory reduce() safe)
        rep['amount'] = float(instance.amount)
        return rep

    def get_organization(self, obj) -> str:
        owner = obj.campaign.owner
        profile = getattr(owner, 'profile', None)
        if profile and getattr(profile, 'ui_name', None):
            return profile.ui_name
        return owner.username
