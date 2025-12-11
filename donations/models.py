from django.db import models
from django.contrib.auth import get_user_model
from campaigns.models import Campaign

User = get_user_model()


class Donation(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.donor.username} donated {self.amount} to {self.campaign.title}"
