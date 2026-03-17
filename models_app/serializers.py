from rest_framework import serializers
from .models import (
    Product, ProductSpec, ProductScore, ProductTrap,
    ProductComment, ProductLike, Post, PostComment, PostLike
)
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
    review_count = serializers.SerializerMethodField()
    trend = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand', 'category_slug', 'image_url',
            'tier', 'tier_score', 'community_tier', 'product_type', 'usage',
            'price_min', 'price_max', 'review_count', 'trend', 'specs', 'scores',
            'view_count', 'like_count'
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

    def get_review_count(self, obj):
        """annotate된 값 우선, 없으면 property 사용"""
        if hasattr(obj, '_annotated_review_count'):
            return obj._annotated_review_count
        return obj.review_count


class ProductDetailSerializer(serializers.ModelSerializer):
    """제품 상세용 시리얼라이저"""
    brand = BrandListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)
    scores = ProductScoreSerializer(many=True, read_only=True)
    traps = ProductTrapSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    prev_version = serializers.SerializerMethodField()
    alternatives = serializers.SerializerMethodField()
    filter_labels = serializers.SerializerMethodField()
    seo_meta = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand', 'category', 'image_url', 'description',
            'tier', 'tier_score', 'community_tier', 'product_type', 'usage',
            'price_min', 'price_max', 'coupang_link', 'naver_link',
            'release_year', 'version_number',
            'specs', 'scores', 'traps', 'review_count', 'prev_version',
            'alternatives', 'filter_labels', 'seo_meta',
            'view_count', 'like_count', 'is_liked',
            'created_at', 'updated_at'
        ]

    def get_review_count(self, obj):
        """annotate된 값 우선, 없으면 property 사용"""
        if hasattr(obj, '_annotated_review_count'):
            return obj._annotated_review_count
        return obj.review_count

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
        ).exclude(id=obj.id).select_related('brand').order_by('-tier_score')[:3]

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

    def get_is_liked(self, obj):
        # ViewSet에서 annotate된 _is_liked 사용 (추가 쿼리 방지)
        if hasattr(obj, '_is_liked'):
            return obj._is_liked
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProductLike.objects.filter(product=obj, user=request.user).exists()
        return False


# 하위 호환성을 위한 별칭
ShoeModelListSerializer = ProductListSerializer
ShoeModelDetailSerializer = ProductDetailSerializer


# ====== 제품 댓글 시리얼라이저 ======

class ProductCommentSerializer(serializers.ModelSerializer):
    """제품 댓글 목록/상세 시리얼라이저"""
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = [
            'id', 'user', 'content', 'like_count',
            'created_at', 'updated_at', 'replies', 'is_owner'
        ]

    def get_user(self, obj):
        profile = getattr(obj.user, 'profile', None)
        # first_name을 별명으로 사용, 없으면 이메일 @ 앞부분
        nickname = obj.user.first_name or obj.user.email.split('@')[0]
        return {
            'id': obj.user.id,
            'username': nickname,
            'badge': profile.badge if profile else 'none',
        }

    def get_replies(self, obj):
        """대댓글 목록 (최대 5개)"""
        if obj.parent is not None:
            return []
        replies = obj.replies.select_related('user', 'user__profile').order_by('created_at')[:5]
        return ProductCommentSerializer(replies, many=True, context=self.context).data

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False


class ProductCommentCreateSerializer(serializers.ModelSerializer):
    """제품 댓글 생성 시리얼라이저"""
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ProductComment
        fields = ['content', 'parent_id']

    def validate_content(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('댓글 내용을 입력해주세요.')
        if len(value) > 1000:
            raise serializers.ValidationError('댓글은 1000자 이하로 작성해주세요.')
        return value.strip()

    def create(self, validated_data):
        product = self.context['product']
        user = self.context['request'].user
        parent_id = validated_data.pop('parent_id', None)

        parent = None
        if parent_id:
            try:
                parent = ProductComment.objects.get(
                    id=parent_id,
                    product=product,
                    parent=None  # 대댓글에는 답글 불가
                )
            except ProductComment.DoesNotExist:
                raise serializers.ValidationError({'parent_id': '존재하지 않는 댓글입니다.'})

        return ProductComment.objects.create(
            product=product,
            user=user,
            parent=parent,
            **validated_data
        )


# ====== 게시판 시리얼라이저 ======

class PostCommentSerializer(serializers.ModelSerializer):
    """게시글 댓글 시리얼라이저"""
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'content', 'created_at', 'replies', 'is_owner']

    def get_user(self, obj):
        profile = getattr(obj.user, 'profile', None)
        nickname = obj.user.first_name or obj.user.email.split('@')[0]
        return {
            'id': obj.user.id,
            'username': nickname,
            'badge': profile.badge if profile else 'none',
        }

    def get_replies(self, obj):
        if obj.parent is not None:
            return []
        # prefetch_related로 미리 로딩된 데이터 활용 (새 쿼리 방지)
        replies = sorted(obj.replies.all(), key=lambda r: r.created_at)[:5]
        return PostCommentSerializer(replies, many=True, context=self.context).data

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False


class PostCommentCreateSerializer(serializers.ModelSerializer):
    """게시글 댓글 생성 시리얼라이저"""
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = PostComment
        fields = ['content', 'parent_id']

    def validate_content(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('댓글 내용을 입력해주세요.')
        return value.strip()

    def create(self, validated_data):
        post = self.context['post']
        user = self.context['request'].user
        parent_id = validated_data.pop('parent_id', None)

        parent = None
        if parent_id:
            try:
                parent = PostComment.objects.get(
                    id=parent_id,
                    post=post,
                    parent=None
                )
            except PostComment.DoesNotExist:
                raise serializers.ValidationError({'parent_id': '존재하지 않는 댓글입니다.'})

        return PostComment.objects.create(
            post=post,
            user=user,
            parent=parent,
            **validated_data
        )


class PostListSerializer(serializers.ModelSerializer):
    """
    게시글 목록 시리얼라이저 (최적화 버전)
    - content_preview: DB Annotation (_content_preview) 또는 content 필드에서 추출
    - user, product_info: select_related로 미리 로딩된 데이터 사용
    """
    user = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_info = serializers.SerializerMethodField()
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'tag', 'user', 'category_slug', 'category_name',
            'product_info', 'view_count', 'like_count', 'comment_count',
            'is_notice', 'created_at', 'rating', 'content_preview'
        ]

    def get_user(self, obj):
        # select_related('user', 'user__profile')로 미리 로딩됨
        profile = getattr(obj.user, 'profile', None)
        nickname = obj.user.first_name or obj.user.email.split('@')[0]
        return {
            'id': obj.user.id,
            'username': nickname,
            'badge': profile.badge if profile else 'none',
        }

    def get_product_info(self, obj):
        # select_related('product', 'product__brand')로 미리 로딩됨
        if not obj.product:
            return None
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'slug': obj.product.slug,
            'brand_name': obj.product.brand.name,
            'tier': obj.product.tier,
        }

    def get_content_preview(self, obj):
        """
        내용 미리보기 (100자)
        - DB Annotation (_content_preview)이 있으면 사용 (최적화)
        - 없으면 content 필드에서 직접 추출 (폴백)
        """
        # DB에서 미리 계산된 값 사용 (defer('content')와 함께 사용)
        if hasattr(obj, '_content_preview') and obj._content_preview:
            preview = obj._content_preview
            return preview + '...' if len(preview) >= 100 else preview
        # 폴백: content 필드 직접 사용
        if hasattr(obj, 'content') and obj.content:
            return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세 시리얼라이저"""
    user = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_info = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'tag', 'content', 'user', 'category_slug', 'category_name',
            'product_info', 'view_count', 'like_count', 'comment_count', 'is_notice',
            'is_owner', 'is_liked', 'rating', 'created_at', 'updated_at'
        ]

    def get_user(self, obj):
        profile = getattr(obj.user, 'profile', None)
        nickname = obj.user.first_name or obj.user.email.split('@')[0]
        return {
            'id': obj.user.id,
            'username': nickname,
            'badge': profile.badge if profile else 'none',
        }

    def get_product_info(self, obj):
        if not obj.product:
            return None
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'slug': obj.product.slug,
            'brand_name': obj.product.brand.name,
            'tier': obj.product.tier,
        }

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False

    def get_is_liked(self, obj):
        # ViewSet에서 annotate된 _is_liked 사용 (추가 쿼리 방지)
        if hasattr(obj, '_is_liked'):
            return obj._is_liked
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """게시글 생성 시리얼라이저"""
    category_slug = serializers.SlugField(write_only=True)
    tag = serializers.ChoiceField(
        choices=Post.TAG_CHOICES,
        default='free',
        required=False,
    )
    product_slug = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=200)
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category_slug', 'tag', 'product_slug', 'rating']

    def validate_content(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('내용을 입력해주세요.')
        return value.strip()

    def validate(self, attrs):
        tag = attrs.get('tag', 'free')
        title = attrs.get('title', '').strip()
        product_slug = attrs.get('product_slug', '')

        # 제품후기가 아닌 경우 제목 필수
        if tag != 'product_review' and not title:
            raise serializers.ValidationError({'title': '제목을 입력해주세요.'})

        # 제품후기인데 product_slug 없으면 에러
        if tag == 'product_review' and not product_slug:
            raise serializers.ValidationError({'product_slug': '제품을 선택해주세요.'})

        return attrs

    def create(self, validated_data):
        from brands.models import Category
        category_slug = validated_data.pop('category_slug')
        product_slug = validated_data.pop('product_slug', None)
        rating = validated_data.pop('rating', None)

        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise serializers.ValidationError({'category_slug': '존재하지 않는 카테고리입니다.'})

        product = None
        if product_slug:
            try:
                product = Product.objects.select_related('brand').get(slug=product_slug)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_slug': '존재하지 않는 제품입니다.'})

        # 제품후기에서 제목이 없으면 자동 생성
        title = validated_data.get('title', '').strip()
        if not title and product:
            title = f"{product.brand.name} {product.name} 후기"
            validated_data['title'] = title

        # 제품후기일 때만 rating 저장
        tag = validated_data.get('tag', 'free')
        if tag == 'product_review' and rating is not None:
            validated_data['rating'] = rating

        return Post.objects.create(
            category=category,
            product=product,
            user=self.context['request'].user,
            **validated_data
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    """게시글 수정 시리얼라이저"""

    class Meta:
        model = Post
        fields = ['title', 'content']

    def validate_title(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('제목을 입력해주세요.')
        return value.strip()

    def validate_content(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('내용을 입력해주세요.')
        return value.strip()
