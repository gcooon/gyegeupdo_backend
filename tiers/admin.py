from django.contrib import admin
from django.utils import timezone
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
    list_display = [
        'title', 'user', 'visibility', 'like_count', 'view_count', 'comment_count',
        'display_promotion_score', 'promotion_status', 'is_featured', 'created_at'
    ]
    list_filter = ['visibility', 'is_featured', 'promotion_status', 'created_at']
    search_fields = ['title', 'description', 'user__email']
    readonly_fields = [
        'uuid', 'slug', 'view_count', 'like_count', 'comment_count',
        'created_at', 'updated_at', 'display_promotion_score', 'display_promotion_progress',
        'promoted_at', 'promoted_by'
    ]
    raw_id_fields = ['user']
    list_editable = ['is_featured', 'promotion_status']
    actions = ['promote_selected', 'reset_promotion_status']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'description', 'user', 'uuid')
        }),
        ('통계', {
            'fields': ('view_count', 'like_count', 'comment_count')
        }),
        ('상태', {
            'fields': ('visibility', 'is_featured')
        }),
        ('승격 시스템', {
            'fields': (
                'display_promotion_score', 'display_promotion_progress',
                'promotion_status', 'promoted_at', 'promoted_by'
            ),
            'classes': ('collapse',)
        }),
        ('타임스탬프', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='승격 점수')
    def display_promotion_score(self, obj):
        return f"{obj.promotion_score:.1f}"

    @admin.display(description='승격 진행률')
    def display_promotion_progress(self, obj):
        progress = obj.promotion_progress
        return f"{progress['status_display']} ({progress['progress_percent']:.1f}%)"

    @admin.action(description='선택한 계급도 승격 처리')
    def promote_selected(self, request, queryset):
        updated = queryset.exclude(promotion_status='promoted').update(
            promotion_status='promoted',
            promoted_at=timezone.now(),
            promoted_by=request.user
        )
        self.message_user(request, f'{updated}개 계급도가 승격 처리되었습니다.')

    @admin.action(description='선택한 계급도 승격 취소 (일반으로)')
    def reset_promotion_status(self, request, queryset):
        updated = queryset.update(
            promotion_status='normal',
            promoted_at=None,
            promoted_by=None
        )
        self.message_user(request, f'{updated}개 계급도의 승격 상태가 초기화되었습니다.')


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
