from django.urls import path
from .views import DonationListCreateView

urlpatterns = [
    path('donations/', DonationListCreateView.as_view(),
         name='donation-list-create'),
]
