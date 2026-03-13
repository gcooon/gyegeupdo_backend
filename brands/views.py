from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Category, Brand
from .serializers import (
    CategorySerializer, CategoryListSerializer,
    BrandListSerializer, BrandDetailSerializer
)


@api_view(['GET'])
def home_summary(request):
    """홈 페이지 전용 요약 API - 모든 데이터를 한 번에 반환"""
    from models_app.models import Product
    from reviews.models import Review
    from tiers.models import TierDispute, UserTierChart

    # 1. 카테고리 목록 + TOP 3 제품
    categories = Category.objects.filter(is_active=True).order_by('display_order')
    categories_data = []

    for cat in categories:
        # TOP 3 제품 조회
        top_products = Product.objects.filter(
            category=cat,
            is_active=True
        ).select_related('brand').order_by('-tier_score')[:3]

        top_items = []
        for p in top_products:
            top_items.append({
                'name': p.name,
                'slug': p.slug,
                'tier': p.tier,
                'score': float(p.tier_score) if p.tier_score else 0,
                'brand_name': p.brand.name if p.brand else '',
                'brand_slug': p.brand.slug if p.brand else '',
                'image_url': p.image_url or '',
                'usage': p.usage or '',
            })

        # 트렌딩 제품 (리뷰 수 기준)
        trending = Product.objects.filter(
            category=cat,
            is_active=True
        ).annotate(
            _review_count=Count('reviews')
        ).order_by('-_review_count').first()

        categories_data.append({
            'slug': cat.slug,
            'name': cat.name,
            'icon': cat.icon,
            'description': cat.description or '',
            'color': cat.display_config.get('color', '#3B82F6') if cat.display_config else '#3B82F6',
            'top_items': top_items,
            'trending': trending.name if trending else '',
        })

    # 2. HOT 이의 제기 (최근 4개, 투표 많은 순)
    disputes = TierDispute.objects.select_related(
        'product', 'product__brand', 'product__category'
    ).order_by('-support_count', '-created_at')[:4]

    disputes_data = []
    for d in disputes:
        total_votes = d.support_count + d.oppose_count
        disputes_data.append({
            'id': d.id,
            'category': d.product.category.slug if d.product.category else '',
            'category_name': d.product.category.name if d.product.category else '',
            'category_icon': d.product.category.icon if d.product.category else '',
            'product_id': d.product.id,
            'product_name': d.product.name,
            'product_slug': d.product.slug,
            'brand_name': d.product.brand.name if d.product.brand else '',
            'current_tier': d.product.tier,
            'proposed_tier': d.proposed_tier,
            'up_votes': d.support_count,
            'down_votes': d.oppose_count,
            'total_votes': total_votes,
            'reason': d.reason or '',
            'days_left': 7,  # TODO: 실제 계산
        })

    # 3. 최신 리뷰 (4개)
    reviews = Review.objects.filter(
        is_visible=True
    ).select_related('user', 'product', 'product__brand', 'product__category').order_by('-created_at')[:4]

    reviews_data = []
    for r in reviews:
        # 사용자 타입 정보 (발볼, 사이즈 등)
        user_type_parts = []
        if r.width_score:
            width_labels = {'narrow': '좁은 발', 'normal': '보통 발', 'wide': '넓은 발'}
            user_type_parts.append(width_labels.get(r.width_score, ''))
        if r.size_fit:
            size_labels = {'half_up': '반 사이즈 업', 'true': '정사이즈', 'half_down': '반 사이즈 다운'}
            user_type_parts.append(size_labels.get(r.size_fit, ''))

        reviews_data.append({
            'id': r.id,
            'category': r.product.category.slug if r.product and r.product.category else '',
            'category_icon': r.product.category.icon if r.product and r.product.category else '',
            'user': {
                'name': r.user.username if r.user else '익명',
                'type': ' / '.join(filter(None, user_type_parts)),
            },
            'product': {
                'name': r.product.name if r.product else '',
                'brand': r.product.brand.name if r.product and r.product.brand else '',
                'tier': r.product.tier if r.product else 'B',
                'slug': r.product.slug if r.product else '',
            },
            'rating': r.fit_score,  # 착화감 점수를 rating으로 사용
            'content': r.comment[:200] if r.comment else '',
            'likes': 0,  # TODO: helpful_count 필드 추가
            'comments': 0,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '',
        })

    # 4. 인기 사용자 계급도 (4개)
    user_charts = UserTierChart.objects.filter(
        visibility='public'
    ).order_by('-like_count', '-view_count')[:4]

    user_charts_data = []
    for uc in user_charts:
        # tier_data는 {"S": [...], "A": [...], ...} 형식
        item_count = sum(len(items) for items in uc.tier_data.values()) if uc.tier_data else 0
        user_charts_data.append({
            'slug': uc.slug,
            'title': uc.title,
            'author': uc.user.username if uc.user else '익명',
            'likes': uc.like_count,
            'views': uc.view_count,
            'items': item_count,
        })

    return Response({
        'success': True,
        'data': {
            'categories': categories_data,
            'disputes': disputes_data,
            'reviews': reviews_data,
            'user_charts': user_charts_data,
        },
        'message': 'OK'
    })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """카테고리 API ViewSet"""
    queryset = Category.objects.filter(is_active=True).order_by('display_order')
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer

    @method_decorator(cache_page(60 * 5))  # 5분 캐시
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().annotate(
            _brand_count=Count('brands', filter=Q(brands__is_active=True), distinct=True),
            _product_count=Count('products', filter=Q(products__is_active=True), distinct=True),
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': len(serializer.data)
            },
            'message': 'OK'
        })

    def retrieve(self, request, *args, **kwargs):
        """단일 카테고리 상세 조회 (slug 기준)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """브랜드 API ViewSet"""
    queryset = Brand.objects.filter(is_active=True).select_related('category').prefetch_related('scores')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BrandDetailSerializer
        return BrandListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        tier = self.request.query_params.get('tier')

        if category:
            queryset = queryset.filter(category__slug=category)
        if tier:
            tiers = tier.split(',')
            queryset = queryset.filter(tier__in=tiers)

        return queryset

    @method_decorator(cache_page(60 * 3))  # 3분 캐시
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().annotate(
            _product_count=Count('products', filter=Q(products__is_active=True), distinct=True),
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """브랜드의 제품 목록 조회"""
        brand = self.get_object()
        from models_app.serializers import ProductListSerializer
        products = brand.products.filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })
