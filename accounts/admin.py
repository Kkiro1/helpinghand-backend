from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'display_name', 'phone')
    list_select_related = ('user',)
    search_fields = ('user__username', 'user__email', 'display_name', 'phone')
    list_filter = ('role',)
