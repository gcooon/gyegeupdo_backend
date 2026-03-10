from rest_framework import serializers
from .models import Category, Brand, BrandScore


class CategorySerializer(serializers.ModelSerializer):
    """카테고리 시리얼라이저 (정의 포함)"""
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'group', 'description',
            'display_config',
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
        fields = [
            'id', 'name', 'slug', 'icon', 'group', 'description',
            'display_config', 'display_order', 'product_count', 'brand_count'
        ]

    def get_product_count(self, obj):
        # annotate된 값이 있으면 사용 (N+1 방지)
        if hasattr(obj, '_product_count'):
            return obj._product_count
        return obj.products.filter(is_active=True).count()

    def get_brand_count(self, obj):
        if hasattr(obj, '_brand_count'):
            return obj._brand_count
        return obj.brands.filter(is_active=True).count()


class BrandScoreSerializer(serializers.ModelSerializer):
    """브랜드 점수 시리얼라이저"""
    class Meta:
        model = BrandScore
        fields = ['key', 'label', 'value']


class BrandListSerializer(serializers.ModelSerializer):
    """브랜드 목록용 시리얼라이저"""
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'logo_url', 'tier', 'tier_score',
            'description', 'category_slug', 'scores'
        ]

    def get_scores(self, obj):
        """동적 BrandScore가 있으면 사용, 없으면 레거시 필드"""
        brand_scores = obj.scores.all()
        if brand_scores:
            return BrandScoreSerializer(brand_scores, many=True).data
        # 레거시 폴백
        return [
            {'key': 'lineup', 'label': '라인업', 'value': obj.lineup_score},
            {'key': 'tech', 'label': '기술력', 'value': obj.tech_score},
            {'key': 'durability', 'label': '내구성', 'value': obj.durability_score},
            {'key': 'community', 'label': '커뮤니티', 'value': obj.community_score},
        ]


class BrandDetailSerializer(serializers.ModelSerializer):
    """브랜드 상세용 시리얼라이저"""
    category = CategoryListSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'logo_url', 'tier', 'tier_score',
            'description', 'category', 'product_count', 'scores', 'updated_at'
        ]

    def get_product_count(self, obj):
        if hasattr(obj, '_product_count'):
            return obj._product_count
        return obj.products.filter(is_active=True).count()

    def get_scores(self, obj):
        brand_scores = obj.scores.all()
        if brand_scores:
            return BrandScoreSerializer(brand_scores, many=True).data
        return [
            {'key': 'lineup', 'label': '라인업', 'value': obj.lineup_score},
            {'key': 'tech', 'label': '기술력', 'value': obj.tech_score},
            {'key': 'durability', 'label': '내구성', 'value': obj.durability_score},
            {'key': 'community', 'label': '커뮤니티', 'value': obj.community_score},
        ]
