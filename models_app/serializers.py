from rest_framework import serializers
from .models import Product, ProductSpec, ProductScore, ProductTrap
from brands.serializers import BrandListSerializer, CategorySerializer


class ProductSpecSerializer(serializers.ModelSerializer):
    """제품 스펙 시리얼라이저"""
    label = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    class Meta:
        model = ProductSpec
        fields = ['key', 'value', 'label', 'unit']

    def get_label(self, obj):
        """카테고리 정의에서 라벨 가져오기"""
        spec_defs = obj.product.category.spec_definitions or []
        for spec_def in spec_defs:
            if spec_def.get('key') == obj.key:
                return spec_def.get('label', obj.key)
        return obj.key

    def get_unit(self, obj):
        """카테고리 정의에서 단위 가져오기"""
        spec_defs = obj.product.category.spec_definitions or []
        for spec_def in spec_defs:
            if spec_def.get('key') == obj.key:
                return spec_def.get('unit', '')
        return ''


class ProductScoreSerializer(serializers.ModelSerializer):
    """제품 점수 시리얼라이저"""
    label = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = ProductScore
        fields = ['key', 'value', 'label', 'weight']

    def get_label(self, obj):
        """카테고리 정의에서 라벨 가져오기"""
        score_defs = obj.product.category.score_definitions or []
        for score_def in score_defs:
            if score_def.get('key') == obj.key:
                return score_def.get('label', obj.key)
        return obj.key

    def get_weight(self, obj):
        """카테고리 정의에서 가중치 가져오기"""
        score_defs = obj.product.category.score_definitions or []
        for score_def in score_defs:
            if score_def.get('key') == obj.key:
                return score_def.get('weight', 0)
        return 0


class ProductTrapSerializer(serializers.ModelSerializer):
    """제품 함정 시리얼라이저"""

    class Meta:
        model = ProductTrap
        fields = ['id', 'trap_type', 'trap_description']


class ProductListSerializer(serializers.ModelSerializer):
    """제품 목록용 시리얼라이저"""
    brand = BrandListSerializer(read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    review_count = serializers.IntegerField(read_only=True, default=0)
    trend = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand', 'category_slug', 'image_url',
            'tier', 'tier_score', 'community_tier', 'product_type', 'usage',
            'price_min', 'price_max', 'review_count', 'trend', 'specs', 'scores'
        ]

    def get_trend(self, obj):
        if hasattr(obj, 'trend_logs'):
            latest_trend = obj.trend_logs.order_by('-recorded_at').first()
            return latest_trend.trend if latest_trend else 'stable'
        return 'stable'

    def get_specs(self, obj):
        """주요 스펙만 딕셔너리로 반환"""
        return {spec.key: spec.value for spec in obj.specs.all()[:5]}

    def get_scores(self, obj):
        """점수를 딕셔너리로 반환"""
        return {score.key: score.value for score in obj.scores.all()}


class ProductDetailSerializer(serializers.ModelSerializer):
    """제품 상세용 시리얼라이저"""
    brand = BrandListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)
    scores = ProductScoreSerializer(many=True, read_only=True)
    traps = ProductTrapSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(read_only=True, default=0)
    prev_version = serializers.SerializerMethodField()
    alternatives = serializers.SerializerMethodField()
    filter_labels = serializers.SerializerMethodField()
    seo_meta = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand', 'category', 'image_url', 'description',
            'tier', 'tier_score', 'community_tier', 'product_type', 'usage',
            'price_min', 'price_max', 'coupang_link', 'naver_link',
            'release_year', 'version_number',
            'specs', 'scores', 'traps', 'review_count', 'prev_version',
            'alternatives', 'filter_labels', 'seo_meta', 'created_at', 'updated_at'
        ]

    def get_prev_version(self, obj):
        if obj.prev_version:
            return {
                'id': obj.prev_version.id,
                'name': obj.prev_version.name,
                'slug': obj.prev_version.slug,
                'tier': obj.prev_version.tier,
                'tier_score': obj.prev_version.tier_score
            }
        return None

    def get_alternatives(self, obj):
        """비슷한 대안 제품 3개 조회"""
        alternatives = Product.objects.filter(
            category=obj.category,
            product_type=obj.product_type,
            is_active=True
        ).exclude(id=obj.id).order_by('-tier_score')[:3]

        return [{
            'id': m.id,
            'name': m.name,
            'slug': m.slug,
            'brand': {'name': m.brand.name, 'slug': m.brand.slug},
            'tier': m.tier,
            'tier_score': m.tier_score,
            'image_url': m.image_url
        } for m in alternatives]

    def get_filter_labels(self, obj):
        """카테고리 정의에서 product_type, usage의 라벨 가져오기"""
        filter_defs = obj.category.filter_definitions or {}
        result = {}

        # product_type 라벨
        type_options = filter_defs.get('product_type', [])
        for option in type_options:
            if option.get('value') == obj.product_type:
                result['product_type'] = option.get('label', obj.product_type)
                break
        if 'product_type' not in result:
            result['product_type'] = obj.product_type

        # usage 라벨
        usage_options = filter_defs.get('usage', [])
        for option in usage_options:
            if option.get('value') == obj.usage:
                result['usage'] = option.get('label', obj.usage)
                break
        if 'usage' not in result:
            result['usage'] = obj.usage

        return result

    def get_seo_meta(self, obj):
        filter_labels = self.get_filter_labels(obj)
        specs = obj.get_specs_dict()

        return {
            'title': f"{obj.brand.name} {obj.name} 계급도 — 2026 {filter_labels.get('usage', '')} {obj.tier}티어",
            'description': f"{obj.name} 스펙, 후기 {getattr(obj, 'review_count', 0)}개 종합. {obj.category.name} 계급도."
        }


# 하위 호환성을 위한 별칭
ShoeModelListSerializer = ProductListSerializer
ShoeModelDetailSerializer = ProductDetailSerializer
