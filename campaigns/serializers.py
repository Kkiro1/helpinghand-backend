from rest_framework import serializers

from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    # Frontend fields (numbers, not strings)
    goal = serializers.SerializerMethodField()
    raised = serializers.SerializerMethodField()
    deadline = serializers.DateField(source='end_date', read_only=True, allow_null=True)

    donors = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'title', 'description',
            'category', 'image',
            'goal', 'raised', 'donors', 'deadline', 'organization',
            # keep old backend fields too
            'goal_amount', 'current_amount', 'start_date', 'end_date',
            'is_active', 'owner', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'current_amount', 'owner', 'created_at', 'updated_at',
            'goal', 'raised', 'deadline', 'donors', 'organization',
        ]

    def get_goal(self, obj) -> float:
        try:
            return float(obj.goal_amount)
        except Exception:
            return 0.0

    def get_raised(self, obj) -> float:
        try:
            return float(obj.current_amount)
        except Exception:
            return 0.0

    def get_donors(self, obj) -> int:
        try:
            from donations.models import Donation
            return Donation.objects.filter(campaign=obj).values('donor_id').distinct().count()
        except Exception:
            return 0

    def get_organization(self, obj) -> str:
        owner = obj.owner
        profile = getattr(owner, 'profile', None)
        if profile and getattr(profile, 'ui_name', None):
            return profile.ui_name
        return owner.username
