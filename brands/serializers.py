from rest_framework import serializers
from .models import Category, Brand


class CategorySerializer(serializers.ModelSerializer):
    """카테고리 시리얼라이저 (정의 포함)"""
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'description',
            'spec_definitions', 'score_definitions', 'brand_score_definitions',
            'quiz_definitions', 'filter_definitions',
            'display_order', 'is_active'
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    """카테고리 목록용 간략 시리얼라이저"""
    product_count = serializers.SerializerMethodField()
    brand_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'product_count', 'brand_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

    def get_brand_count(self, obj):
        return obj.brands.filter(is_active=True).count()


class BrandListSerializer(serializers.ModelSerializer):
    """브랜드 목록용 시리얼라이저"""
    category_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'logo_url', 'tier', 'tier_score',
            'lineup_score', 'tech_score', 'durability_score', 'community_score',
            'category_slug'
        ]


class BrandDetailSerializer(serializers.ModelSerializer):
    """브랜드 상세용 시리얼라이저"""
    category = CategoryListSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'logo_url', 'tier', 'tier_score',
            'lineup_score', 'tech_score', 'durability_score', 'community_score',
            'description', 'category', 'product_count', 'updated_at'
        ]

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()
