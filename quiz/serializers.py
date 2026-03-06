from rest_framework import serializers
from .models import QuizSession
from models_app.models import Product


class QuizInputSerializer(serializers.Serializer):
    """퀴즈 입력 시리얼라이저 - 카테고리별로 동적 필드 처리"""
    category = serializers.CharField(required=False, default='running-shoes')
    answers = serializers.DictField(child=serializers.CharField())
    budget_max = serializers.IntegerField(min_value=0, required=False)


class QuizResultSerializer(serializers.ModelSerializer):
    """퀴즈 결과 시리얼라이저"""
    recommendations = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()

    class Meta:
        model = QuizSession
        fields = ['session_key', 'recommendations', 'share_url']

    def get_recommendations(self, obj):
        from models_app.models import Product
        from brands.models import Category

        # 카테고리 기반 추천 로직
        category_slug = obj.answers.get('category', 'running-shoes') if obj.answers else 'running-shoes'

        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return []

        # 제품 조회
        queryset = Product.objects.filter(
            is_active=True,
            category=category
        ).select_related('brand')

        # 답변 기반 필터링
        if obj.answers:
            for key, value in obj.answers.items():
                if key == 'category':
                    continue
                if key == 'product_type' and value:
                    queryset = queryset.filter(product_type=value)
                elif key == 'usage' and value:
                    queryset = queryset.filter(usage=value)

        if obj.budget_max:
            queryset = queryset.filter(price_min__lte=obj.budget_max)

        # 티어 점수 기준 정렬
        top_products = queryset.order_by('-tier_score')[:3]

        recommendations = []
        for rank, product in enumerate(top_products, 1):
            recommendations.append({
                'rank': rank,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'tier': product.tier,
                    'tier_score': product.tier_score,
                    'brand_name': product.brand.name,
                    'image_url': product.image_url
                },
                'reason': [f"{product.tier}티어 제품", f"{product.brand.name} 브랜드"],
                'similar_user_count': 157  # TODO: 실제 계산
            })

        return recommendations

    def get_share_url(self, obj):
        return f"https://gyegeupdo.kr/quiz/result/{obj.session_key}"
