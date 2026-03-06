from django.contrib import admin
from .models import Product, ProductSpec, ProductScore, ProductTrap


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 1


class ProductScoreInline(admin.TabularInline):
    model = ProductScore
    extra = 1


class ProductTrapInline(admin.TabularInline):
    model = ProductTrap
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'tier', 'tier_score', 'product_type', 'usage', 'is_active']
    list_filter = ['tier', 'category', 'brand', 'product_type', 'usage', 'is_active']
    search_fields = ['name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductSpecInline, ProductScoreInline, ProductTrapInline]
    fieldsets = (
        ('기본 정보', {
            'fields': ('brand', 'category', 'name', 'slug', 'image_url', 'description', 'is_active')
        }),
        ('분류', {
            'fields': ('product_type', 'usage')
        }),
        ('티어', {
            'fields': ('tier', 'tier_score', 'community_tier')
        }),
        ('가격 및 링크', {
            'fields': ('price_min', 'price_max', 'coupang_link', 'naver_link')
        }),
        ('버전 정보', {
            'fields': ('release_year', 'version_number', 'prev_version'),
            'classes': ('collapse',)
        }),
        ('날짜', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    list_filter = ['key']
    search_fields = ['product__name', 'key']


@admin.register(ProductScore)
class ProductScoreAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    list_filter = ['key']
    search_fields = ['product__name', 'key']


@admin.register(ProductTrap)
class ProductTrapAdmin(admin.ModelAdmin):
    list_display = ['product', 'trap_type', 'created_at']
    list_filter = ['trap_type']
    search_fields = ['product__name', 'trap_description']
