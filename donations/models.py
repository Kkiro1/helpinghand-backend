from django.db import models
from django.contrib.auth import get_user_model

from campaigns.models import Campaign

User = get_user_model()


class Donation(models.Model):
    PAYMENT_CARD = 'card'
    PAYMENT_PAYPAL = 'paypal'

    PAYMENT_CHOICES = [
        (PAYMENT_CARD, 'Card'),
        (PAYMENT_PAYPAL, 'PayPal'),
    ]

    STATUS_COMPLETED = 'Completed'
    STATUS_PENDING = 'Pending'
    STATUS_FAILED = 'Failed'

    STATUS_CHOICES = [
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_FAILED, 'Failed'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # UI fields used by the current frontend
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_CARD)
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.donor.username} donated {self.amount} to {self.campaign.title}"
