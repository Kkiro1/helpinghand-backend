from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Campaign(models.Model):
    """
    A donation campaign (e.g. help for a family, hospital, etc.)
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    # UI fields used by the current frontend
    category = models.CharField(max_length=50, blank=True, default='')
    image = models.CharField(max_length=10, blank=True, default='')  # emoji or short string


    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    # Who created this campaign
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
