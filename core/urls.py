from django.urls import path
from . import views

# you can keep or remove app_name, doesn't matter here
# app_name = 'core'

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
]
