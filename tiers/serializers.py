from rest_framework import serializers
from .models import TierDispute, DisputeVote, TrendLog, UserTierChart, TierChartComment, TierChartLike


class TierDisputeListSerializer(serializers.ModelSerializer):
    """이의제기 목록 시리얼라이저"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_badge = serializers.CharField(source='user.profile.badge', read_only=True, default='none')
    dispute_type_display = serializers.CharField(source='get_dispute_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TierDispute
        fields = [
            'id', 'product_name', 'user_badge', 'dispute_type', 'dispute_type_display',
            'reason', 'support_count', 'oppose_count', 'status', 'status_display',
            'created_at'
        ]


class TierDisputeCreateSerializer(serializers.ModelSerializer):
    """이의제기 생성 시리얼라이저"""
    class Meta:
        model = TierDispute
        fields = ['product', 'dispute_type', 'reason', 'evidence_url']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DisputeVoteSerializer(serializers.ModelSerializer):
    """투표 시리얼라이저"""
    class Meta:
        model = DisputeVote
        fields = ['vote']


class TrendLogSerializer(serializers.ModelSerializer):
    """트렌드 로그 시리얼라이저"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    brand_name = serializers.CharField(source='product.brand.name', read_only=True)
    tier = serializers.CharField(source='product.tier', read_only=True)
    image_url = serializers.CharField(source='product.image_url', read_only=True)
    score_change = serializers.FloatField(read_only=True)
    trend_display = serializers.CharField(source='get_trend_display', read_only=True)

    class Meta:
        model = TrendLog
        fields = [
            'product_name', 'product_slug', 'brand_name', 'tier', 'image_url',
            'trend', 'trend_display', 'score_change', 'rank', 'recorded_at'
        ]


# ===== 사용자 계급도 시리얼라이저 =====

class TierChartCommentSerializer(serializers.ModelSerializer):
    """계급도 댓글 시리얼라이저"""
    user_nickname = serializers.CharField(source='user.first_name', read_only=True)
    user_badge = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = TierChartComment
        fields = [
            'id', 'user_nickname', 'user_badge', 'content', 'like_count',
            'created_at', 'updated_at', 'parent', 'replies', 'is_owner'
        ]
        read_only_fields = ['like_count', 'created_at', 'updated_at']

    def get_user_badge(self, obj):
        try:
            return obj.user.profile.badge
        except Exception:
            return 'none'

    def get_replies(self, obj):
        if obj.parent is None:  # 최상위 댓글만 답글 표시
            replies = obj.replies.all()[:5]  # 최대 5개 답글
            return TierChartCommentSerializer(replies, many=True, context=self.context).data
        return []

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False


class TierChartCommentCreateSerializer(serializers.ModelSerializer):
    """댓글 생성 시리얼라이저"""
    class Meta:
        model = TierChartComment
        fields = ['content', 'parent']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['tier_chart'] = self.context['tier_chart']
        return super().create(validated_data)


class UserTierChartListSerializer(serializers.ModelSerializer):
    """사용자 계급도 목록 시리얼라이저"""
    user_nickname = serializers.CharField(source='user.first_name', read_only=True)
    user_badge = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    promotion_score = serializers.FloatField(read_only=True)
    promotion_status = serializers.CharField(read_only=True)
    promotion_status_display = serializers.CharField(
        source='get_promotion_status_display', read_only=True
    )
    promotion_progress = serializers.SerializerMethodField()
    # HOT/명예의전당 필드
    hot_until = serializers.DateTimeField(read_only=True)
    hall_of_fame_at = serializers.DateTimeField(read_only=True)
    # 국제화 필드
    language = serializers.CharField(read_only=True)
    language_display = serializers.CharField(source='get_language_display', read_only=True)
    author_country = serializers.CharField(read_only=True)

    class Meta:
        model = UserTierChart
        fields = [
            'id', 'uuid', 'slug', 'title', 'description',
            'user_nickname', 'user_badge', 'item_count',
            'view_count', 'like_count', 'comment_count',
            'is_liked', 'is_featured', 'created_at',
            'promotion_score', 'promotion_status', 'promotion_status_display',
            'promotion_progress', 'hot_until', 'hall_of_fame_at',
            # 국제화
            'language', 'language_display', 'author_country'
        ]

    def get_user_badge(self, obj):
        try:
            return obj.user.profile.badge
        except Exception:
            return 'none'

    def get_item_count(self, obj):
        count = 0
        if obj.tier_data:
            for tier_items in obj.tier_data.values():
                if isinstance(tier_items, list):
                    count += len(tier_items)
        return count

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TierChartLike.objects.filter(
                tier_chart=obj, user=request.user
            ).exists()
        return False

    def get_promotion_progress(self, obj):
        """간소화된 승격 진행률 (목록용)"""
        progress = obj.promotion_progress
        return {
            'current_score': progress['current_score'],
            'progress_percent': progress['progress_percent'],
            'status': progress['status'],
            'status_display': progress['status_display'],
        }


class UserTierChartDetailSerializer(serializers.ModelSerializer):
    """사용자 계급도 상세 시리얼라이저"""
    user_nickname = serializers.CharField(source='user.first_name', read_only=True)
    user_badge = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    share_url = serializers.CharField(read_only=True)
    promotion_score = serializers.FloatField(read_only=True)
    promotion_status = serializers.CharField(read_only=True)
    promotion_status_display = serializers.CharField(
        source='get_promotion_status_display', read_only=True
    )
    promotion_progress = serializers.SerializerMethodField()
    # HOT/명예의전당 필드
    hot_until = serializers.DateTimeField(read_only=True)
    hall_of_fame_at = serializers.DateTimeField(read_only=True)
    converted_to_official = serializers.BooleanField(read_only=True)
    converted_category_slug = serializers.CharField(read_only=True)
    # 국제화 필드
    language = serializers.CharField(read_only=True)
    language_display = serializers.CharField(source='get_language_display', read_only=True)
    author_country = serializers.CharField(read_only=True)
    is_global = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserTierChart
        fields = [
            'id', 'uuid', 'slug', 'title', 'description', 'tier_data',
            'user_nickname', 'user_badge',
            'view_count', 'like_count', 'comment_count',
            'visibility', 'is_featured', 'is_liked', 'is_owner',
            'share_url', 'comments', 'created_at', 'updated_at',
            'promotion_score', 'promotion_status', 'promotion_status_display',
            'promotion_progress', 'hot_until', 'hall_of_fame_at',
            'converted_to_official', 'converted_category_slug',
            # 국제화
            'language', 'language_display', 'author_country', 'is_global'
        ]

    def get_user_badge(self, obj):
        try:
            return obj.user.profile.badge
        except Exception:
            return 'none'

    def get_comments(self, obj):
        # 최상위 댓글만 (최신 10개)
        comments = obj.comments.filter(parent=None).order_by('-created_at')[:10]
        return TierChartCommentSerializer(
            comments, many=True, context=self.context
        ).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TierChartLike.objects.filter(
                tier_chart=obj, user=request.user
            ).exists()
        return False

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def get_promotion_progress(self, obj):
        """상세 승격 진행률 (점수 breakdown 포함)"""
        return obj.promotion_progress


class UserTierChartCreateSerializer(serializers.ModelSerializer):
    """사용자 계급도 생성 시리얼라이저"""
    class Meta:
        model = UserTierChart
        fields = ['title', 'description', 'tier_data', 'visibility', 'language']

    def validate_tier_data(self, value):
        """티어 데이터 검증"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("티어 데이터는 객체 형식이어야 합니다.")

        valid_tiers = ['S', 'A', 'B', 'C', 'D']
        for tier in value.keys():
            if tier not in valid_tiers:
                raise serializers.ValidationError(f"유효하지 않은 티어: {tier}")
            if not isinstance(value[tier], list):
                raise serializers.ValidationError(f"티어 {tier}의 값은 배열이어야 합니다.")

        # 최소 1개 아이템 필요
        total_items = sum(len(items) for items in value.values())
        if total_items == 0:
            raise serializers.ValidationError("최소 1개 이상의 아이템이 필요합니다.")

        return value

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("제목은 2자 이상이어야 합니다.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        # 사용자 프로필에서 국가 정보 자동 설정
        try:
            if hasattr(user, 'profile') and user.profile.country:
                validated_data['author_country'] = user.profile.country
        except Exception:
            pass
        return super().create(validated_data)


class UserTierChartUpdateSerializer(serializers.ModelSerializer):
    """사용자 계급도 수정 시리얼라이저"""
    class Meta:
        model = UserTierChart
        fields = ['title', 'description', 'tier_data', 'visibility', 'language']

    def validate_tier_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("티어 데이터는 객체 형식이어야 합니다.")
        return value
