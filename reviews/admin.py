from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'fit_score', 'size_fit', 'is_visible', 'created_at']
    list_filter = ['is_visible', 'size_fit', 'width_score', 'created_at']
    search_fields = ['product__name', 'user__email', 'comment']
    readonly_fields = ['weight_multiplier', 'created_at', 'updated_at']
    raw_id_fields = ['product', 'user']
