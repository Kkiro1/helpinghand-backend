from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OrgCampaign(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='org_campaigns')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    goal = models.CharField(max_length=255)  # e.g., "500 Coats"
    duration = models.CharField(max_length=255, blank=True, default='')  # e.g., "Dec 1 - Jan 30"
    notes = models.CharField(max_length=255, blank=True, default='')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class OrgDonation(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_DELIVERED = 'Delivered'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='org_donations')
    campaign = models.ForeignKey(OrgCampaign, on_delete=models.SET_NULL, null=True, blank=True)

    donor = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.donor} -> {self.item}"
