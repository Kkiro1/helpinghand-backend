from django.urls import path

from . import views

urlpatterns = [
    path('org/campaigns/', views.OrgCampaignListCreateView.as_view(), name='org-campaigns'),
    path('org/campaigns/<int:pk>/', views.OrgCampaignDetailView.as_view(), name='org-campaign-detail'),

    path('org/donations/', views.OrgDonationListCreateView.as_view(), name='org-donations'),
    path('org/donations/<int:pk>/', views.OrgDonationDetailView.as_view(), name='org-donation-detail'),

    path('org/profile/', views.org_profile_view, name='org-profile'),
]
