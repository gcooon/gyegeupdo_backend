from django.contrib import admin
from .models import Category, Brand, BrandScore


class BrandScoreInline(admin.TabularInline):
    model = BrandScore
    extra = 0
    fields = ['key', 'label', 'value']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug', 'display_order', 'is_active', 'brand_count']
    list_filter = ['is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'slug', 'icon', 'description', 'display_order', 'is_active')
        }),
        ('프론트엔드 표시 설정', {
            'fields': ('display_config',),
            'description': 'color, heroTitle, heroDescription, heroSubDescription, itemLabel, quizCTA, stats 등',
        }),
        ('브랜드 점수 정의', {
            'fields': ('brand_score_definitions',),
            'description': '[{"key": "heritage", "label": "역사/전통", "weight": 25}, ...]',
        }),
        ('제품 스펙/점수/필터 정의', {
            'fields': ('spec_definitions', 'score_definitions', 'filter_definitions'),
            'classes': ('collapse',),
        }),
        ('퀴즈 정의', {
            'fields': ('quiz_definitions',),
            'classes': ('collapse',),
        }),
    )

    def brand_count(self, obj):
        return obj.brands.filter(is_active=True).count()
    brand_count.short_description = '브랜드 수'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'tier', 'tier_score', 'is_active', 'updated_at']
    list_filter = ['tier', 'category', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['tier_score', 'tier', 'updated_at', 'created_at']
    inlines = [BrandScoreInline]
    fieldsets = (
        ('기본 정보', {
            'fields': ('category', 'name', 'slug', 'logo_url', 'description', 'is_active')
        }),
        ('자동 계산 (BrandScore 기반)', {
            'fields': ('tier', 'tier_score'),
        }),
        ('레거시 점수 (BrandScore 없을 때만 사용)', {
            'fields': ('lineup_score', 'tech_score', 'durability_score', 'community_score'),
            'classes': ('collapse',),
        }),
        ('날짜', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BrandScore)
class BrandScoreAdmin(admin.ModelAdmin):
    list_display = ['brand', 'key', 'label', 'value']
    list_filter = ['brand__category', 'key']
    search_fields = ['brand__name', 'key']
