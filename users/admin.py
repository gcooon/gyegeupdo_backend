from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'foot_width', 'pronation', 'badge', 'review_count', 'total_km']
    list_filter = ['badge', 'foot_width', 'pronation', 'usage_type']
    search_fields = ['user__email']
    readonly_fields = ['review_weight', 'created_at', 'updated_at']
    raw_id_fields = ['user']
