from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "goal_amount", "current_amount", "is_active", "start_date", "end_date")
    list_filter = ("is_active", "category")
    search_fields = ("title", "description", "owner__username")
