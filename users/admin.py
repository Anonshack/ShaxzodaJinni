from django.contrib import admin
from users.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['user__username', 'email', 'phone_number']
    list_filter = ['user__is_active']
