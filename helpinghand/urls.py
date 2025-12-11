from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core (health etc.)
    path('api/', include('core.urls')),

    # Authentication
    path('api/auth/', include('accounts.urls')),

    # Campaigns
    path('api/', include('campaigns.urls')),
]
