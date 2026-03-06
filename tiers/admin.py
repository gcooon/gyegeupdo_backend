from django.contrib import admin
from .models import TierDispute, DisputeVote, TrendLog, UserTierChart, TierChartComment, TierChartLike


@admin.register(TierDispute)
class TierDisputeAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'dispute_type', 'status', 'support_count', 'oppose_count', 'created_at']
    list_filter = ['status', 'dispute_type', 'created_at']
    search_fields = ['product__name', 'user__email', 'reason']
    readonly_fields = ['support_count', 'oppose_count', 'created_at', 'resolved_at']
    raw_id_fields = ['product', 'user']


@admin.register(DisputeVote)
class DisputeVoteAdmin(admin.ModelAdmin):
    list_display = ['dispute', 'user', 'vote', 'created_at']
    list_filter = ['vote', 'created_at']
    search_fields = ['dispute__product__name', 'user__email']
    readonly_fields = ['created_at']
    raw_id_fields = ['dispute', 'user']


@admin.register(TrendLog)
class TrendLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'period', 'trend', 'score', 'prev_score', 'rank', 'recorded_at']
    list_filter = ['period', 'trend', 'recorded_at']
    search_fields = ['product__name']
    readonly_fields = ['recorded_at']
    raw_id_fields = ['product']


@admin.register(UserTierChart)
class UserTierChartAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'visibility', 'like_count', 'view_count', 'comment_count', 'is_featured', 'created_at']
    list_filter = ['visibility', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'user__email']
    readonly_fields = ['uuid', 'slug', 'view_count', 'like_count', 'comment_count', 'created_at', 'updated_at']
    raw_id_fields = ['user']
    list_editable = ['is_featured']


@admin.register(TierChartComment)
class TierChartCommentAdmin(admin.ModelAdmin):
    list_display = ['tier_chart', 'user', 'content_preview', 'like_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__email', 'tier_chart__title']
    readonly_fields = ['like_count', 'created_at', 'updated_at']
    raw_id_fields = ['tier_chart', 'user', 'parent']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '내용'


@admin.register(TierChartLike)
class TierChartLikeAdmin(admin.ModelAdmin):
    list_display = ['tier_chart', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['tier_chart__title', 'user__email']
    readonly_fields = ['created_at']
    raw_id_fields = ['tier_chart', 'user']
