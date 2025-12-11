from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Campaign
        fields = [
            'id',
            'title',
            'description',
            'goal_amount',
            'current_amount',
            'start_date',
            'end_date',
            'is_active',
            'owner',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'current_amount',
                            'owner', 'created_at', 'updated_at']
