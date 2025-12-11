from django.urls import path
from .views import CampaignListCreateView, CampaignDetailView

urlpatterns = [
    path('campaigns/', CampaignListCreateView.as_view(),
         name='campaign-list-create'),
    path('campaigns/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
]
