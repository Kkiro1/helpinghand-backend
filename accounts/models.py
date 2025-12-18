from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """User profile that matches the current frontend expectations."""

    ROLE_DONOR = 'donor'
    ROLE_RECIPIENT = 'recipient'
    ROLE_BOTH = 'both'
    ROLE_ORGANIZATION = 'organization'

    ROLE_CHOICES = [
        (ROLE_DONOR, 'Donor'),
        (ROLE_RECIPIENT, 'Recipient'),
        (ROLE_BOTH, 'Both'),
        (ROLE_ORGANIZATION, 'Organization'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_DONOR,
    )

    # Organization-style profile fields (also usable as display info for individuals)
    display_name = models.CharField(max_length=255, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

    @property
    def ui_name(self) -> str:
        """Best-effort display name for the UI."""
        if self.display_name:
            return self.display_name
        full = (self.user.get_full_name() or '').strip()
        return full if full else self.user.username
