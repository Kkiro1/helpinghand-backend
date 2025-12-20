from django.contrib import admin

from .models import OrgCampaign, OrgDonation


@admin.register(OrgCampaign)
class OrgCampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'status', 'goal', 'duration', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'owner__username')


@admin.register(OrgDonation)
class OrgDonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'item', 'owner', 'status', 'campaign', 'created_at')
    list_filter = ('status',)
    search_fields = ('donor', 'item', 'owner__username')
