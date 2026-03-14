from rest_framework import serializers
from .models import QuizSession
from models_app.models import Product
from brands.models import Category


class QuizInputSerializer(serializers.Serializer):
    """퀴즈 입력 시리얼라이저 - 카테고리별로 동적 필드 처리"""
    category = serializers.CharField(required=False, default='running-shoes')
    answers = serializers.DictField(child=serializers.CharField(), required=False, default=dict)
    budget_max = serializers.IntegerField(min_value=0, required=False, allow_null=True)


class QuizResultSerializer(serializers.ModelSerializer):
    """퀴즈 결과 시리얼라이저"""
    recommendations = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = QuizSession
        fields = ['session_key', 'category', 'recommendations', 'share_url']

    def get_category(self, obj):
        if obj.category:
            return {
                'slug': obj.category.slug,
                'name': obj.category.name,
                'icon': obj.category.icon,
            }
        return None

    def get_recommendations(self, obj):
        """카테고리별 추천 로직"""
        if not obj.category:
            return []

        category = obj.category
        answers = obj.answers or {}

        # 카테고리별 맞춤 추천 로직 적용
        if category.slug == 'running-shoes':
            return self._recommend_running_shoes(category, answers, obj.budget_max)
        elif category.slug == 'chicken':
            return self._recommend_chicken(category, answers)
        elif category.slug == 'mens-watch':
            return self._recommend_watches(category, answers, obj.budget_max)
        else:
            return self._recommend_generic(category, answers, obj.budget_max)

    def _recommend_running_shoes(self, category, answers, budget_max):
        """러닝화 추천 로직"""
        queryset = Product.objects.filter(
            is_active=True,
            category=category
        ).select_related('brand')

        # 답변 기반 필터링 및 점수 조정
        usage = answers.get('usage')
        experience = answers.get('experience')
        priority = answers.get('priority')
        foot_type = answers.get('foot_type')

        if usage:
            queryset = queryset.filter(usage=usage)

        if budget_max:
            queryset = queryset.filter(price_min__lte=budget_max)

        # 점수 기반 정렬 및 필터링
        products = list(queryset.order_by('-tier_score')[:10])

        # 추천 이유 생성
        recommendations = []
        for rank, product in enumerate(products[:3], 1):
            reasons = self._generate_running_shoe_reasons(product, answers)
            recommendations.append(self._format_recommendation(rank, product, reasons))

        return recommendations

    def _recommend_chicken(self, category, answers):
        """치킨 추천 로직"""
        queryset = Product.objects.filter(
            is_active=True,
            category=category
        ).select_related('brand')

        # 답변 기반 필터링
        flavor = answers.get('flavor')  # 맛 선호
        occasion = answers.get('occasion')  # 상황
        texture = answers.get('texture')  # 식감

        # flavor에 따른 product_type 매핑
        flavor_type_map = {
            'original': 'fried',
            'sweet': 'seasoned',
            'spicy': 'seasoned',
            'garlic': 'garlic',
            'soy': 'soy',
        }

        if flavor and flavor in flavor_type_map:
            queryset = queryset.filter(product_type=flavor_type_map[flavor])

        # occasion에 따른 usage 매핑
        occasion_usage_map = {
            'alone': 'solo',
            'couple': 'beer',
            'party': 'family',
            'meal': 'family',
        }

        if occasion and occasion in occasion_usage_map:
            queryset = queryset.filter(usage=occasion_usage_map[occasion])

        products = list(queryset.order_by('-tier_score')[:10])

        recommendations = []
        for rank, product in enumerate(products[:3], 1):
            reasons = self._generate_chicken_reasons(product, answers)
            recommendations.append(self._format_recommendation(rank, product, reasons))

        return recommendations

    def _recommend_watches(self, category, answers, budget_max):
        """시계 추천 로직"""
        queryset = Product.objects.filter(
            is_active=True,
            category=category
        ).select_related('brand')

        # 답변 기반 필터링
        style = answers.get('style')
        purpose = answers.get('purpose')

        # style에 따른 product_type 매핑
        style_type_map = {
            'classic': 'dress',
            'sporty': 'sport',
            'modern': 'chrono',
            'luxury': 'dress',
        }

        if style and style in style_type_map:
            queryset = queryset.filter(product_type=style_type_map[style])

        # purpose에 따른 usage 필터링
        if purpose:
            queryset = queryset.filter(usage=purpose)

        if budget_max:
            queryset = queryset.filter(price_min__lte=budget_max)

        products = list(queryset.order_by('-tier_score')[:10])

        recommendations = []
        for rank, product in enumerate(products[:3], 1):
            reasons = self._generate_watch_reasons(product, answers)
            recommendations.append(self._format_recommendation(rank, product, reasons))

        return recommendations

    def _recommend_generic(self, category, answers, budget_max):
        """일반 카테고리 추천 로직"""
        queryset = Product.objects.filter(
            is_active=True,
            category=category
        ).select_related('brand')

        # 공통 필터 적용
        for key, value in answers.items():
            if key == 'product_type' and value:
                queryset = queryset.filter(product_type=value)
            elif key == 'usage' and value:
                queryset = queryset.filter(usage=value)

        if budget_max:
            queryset = queryset.filter(price_min__lte=budget_max)

        products = list(queryset.order_by('-tier_score')[:3])

        recommendations = []
        for rank, product in enumerate(products, 1):
            reasons = [f"{product.tier}티어 제품", f"{product.brand.name} 브랜드 추천"]
            recommendations.append(self._format_recommendation(rank, product, reasons))

        return recommendations

    def _format_recommendation(self, rank, product, reasons):
        """추천 결과 포맷팅"""
        return {
            'rank': rank,
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'tier': product.tier,
                'tier_score': product.tier_score,
                'brand_name': product.brand.name,
                'brand_slug': product.brand.slug,
                'image_url': product.image_url,
                'usage': product.usage,
                'product_type': product.product_type,
            },
            'match_score': max(75, min(99, 95 - (rank - 1) * 7)),
            'reasons': reasons,
            'review_count': product.reviews.count() if hasattr(product, 'reviews') else 0,
        }

    def _generate_running_shoe_reasons(self, product, answers):
        """러닝화 추천 이유 생성"""
        reasons = []

        usage_labels = {
            'beginner': '입문자에게 추천',
            'daily': '데일리 트레이닝에 최적',
            'tempo': '속도 훈련에 적합',
            'race': '레이스/대회용',
            'long': '장거리 훈련에 최적',
            'recovery': '회복 런에 적합',
        }

        if product.usage in usage_labels:
            reasons.append(usage_labels[product.usage])

        if product.tier in ['S', 'A']:
            reasons.append(f"{product.tier}티어 - 검증된 성능")

        reasons.append(f"{product.brand.name}의 인기 모델")

        return reasons[:3]

    def _generate_chicken_reasons(self, product, answers):
        """치킨 추천 이유 생성"""
        reasons = []

        type_labels = {
            'fried': '바삭한 후라이드',
            'seasoned': '감칠맛 양념',
            'soy': '짭짤한 간장맛',
            'cheese': '고소한 치즈',
            'garlic': '풍미 가득 마늘',
            'roasted': '담백한 구이',
        }

        if product.product_type in type_labels:
            reasons.append(type_labels[product.product_type])

        usage_labels = {
            'solo': '혼닭에 딱',
            'beer': '치맥 필수템',
            'family': '여럿이 함께',
            'latenight': '야식으로 최고',
            'value': '가성비 갑',
        }

        if product.usage in usage_labels:
            reasons.append(usage_labels[product.usage])

        if product.tier in ['S', 'A']:
            reasons.append(f"{product.brand.name} 대표 메뉴")

        return reasons[:3]

    def _generate_watch_reasons(self, product, answers):
        """시계 추천 이유 생성"""
        reasons = []

        type_labels = {
            'dress': '격식있는 자리에 어울림',
            'sport': '활동적인 스타일',
            'diver': '견고한 방수 성능',
            'pilot': '클래식한 항공 디자인',
            'chrono': '실용적인 크로노그래프',
        }

        if product.product_type in type_labels:
            reasons.append(type_labels[product.product_type])

        if product.tier == 'S':
            reasons.append('하이엔드 명품 시계')
        elif product.tier == 'A':
            reasons.append('럭셔리 브랜드')
        elif product.tier == 'B':
            reasons.append('프리미엄 가성비')

        reasons.append(f"{product.brand.name} 인기 모델")

        return reasons[:3]

    def get_share_url(self, obj):
        return f"https://gyegeupdo.kr/quiz/result/{obj.session_key}"
