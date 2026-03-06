from django.contrib import admin
from .models import Category, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'tier', 'tier_score', 'is_active', 'updated_at']
    list_filter = ['tier', 'category', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['tier_score', 'tier', 'updated_at', 'created_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('category', 'name', 'slug', 'logo_url', 'description', 'is_active')
        }),
        ('점수', {
            'fields': ('lineup_score', 'tech_score', 'durability_score', 'community_score')
        }),
        ('자동 계산', {
            'fields': ('tier', 'tier_score'),
            'classes': ('collapse',)
        }),
        ('날짜', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
