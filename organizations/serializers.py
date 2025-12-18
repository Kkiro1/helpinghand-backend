from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserProfile
from .models import OrgCampaign, OrgDonation

User = get_user_model()


class OrgCampaignSerializer(serializers.ModelSerializer):
    donors = serializers.SerializerMethodField()

    class Meta:
        model = OrgCampaign
        fields = ['id', 'title', 'description', 'goal', 'status', 'donors', 'duration', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'donors', 'created_at', 'updated_at']

    def get_donors(self, obj) -> int:
        return OrgDonation.objects.filter(campaign=obj).values('donor').distinct().count()


class OrgDonationSerializer(serializers.ModelSerializer):
    campaignId = serializers.SerializerMethodField()

    class Meta:
        model = OrgDonation
        fields = ['id', 'donor', 'item', 'description', 'campaignId', 'campaign', 'status', 'created_at']
        read_only_fields = ['id', 'campaignId', 'created_at']

    def get_campaignId(self, obj):
        return obj.campaign_id


class OrgProfileSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        user = instance
        profile = getattr(user, 'profile', None)
        return {
            'name': getattr(profile, 'display_name', '') or (user.get_full_name() or user.username),
            'address': getattr(profile, 'address', ''),
            'phone': getattr(profile, 'phone', ''),
            'email': user.email,
            'description': getattr(profile, 'description', ''),
        }

    def update(self, instance, validated_data):
        user = instance
        profile, _ = UserProfile.objects.get_or_create(user=user)

        if 'name' in validated_data:
            profile.display_name = validated_data.get('name', '')
        if 'address' in validated_data:
            profile.address = validated_data.get('address', '')
        if 'phone' in validated_data:
            profile.phone = validated_data.get('phone', '')
        if 'description' in validated_data:
            profile.description = validated_data.get('description', '')
        profile.save()

        if 'email' in validated_data:
            user.email = validated_data.get('email')
            user.save()

        password = validated_data.get('password')
        if password:
            user.set_password(password)
            user.save()

        return user
