from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """제품 API ViewSet"""
    queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
    lookup_field = 'slug'
    pagination_class = ProductPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('specs', 'scores')

        # 필터링
        params = self.request.query_params
        category = params.get('category')
        tier = params.get('tier')
        product_type = params.get('product_type')
        usage = params.get('usage')
        price_max = params.get('price_max')
        brand = params.get('brand')

        if category:
            queryset = queryset.filter(category__slug=category)
        if tier:
            tiers = tier.split(',')
            queryset = queryset.filter(tier__in=tiers)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if usage:
            queryset = queryset.filter(usage=usage)
        if price_max:
            queryset = queryset.filter(price_min__lte=int(price_max))
        if brand:
            queryset = queryset.filter(brand__slug=brand)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                'success': True,
                'data': {
                    'count': paginated_response.data['count'],
                    'results': paginated_response.data['results'],
                    'next': paginated_response.data['next'],
                    'previous': paginated_response.data['previous']
                },
                'message': 'OK'
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {'count': len(serializer.data), 'results': serializer.data},
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

    @action(detail=False, methods=['get'])
    def compare(self, request):
        """두 제품 비교"""
        models_param = request.query_params.get('models', '')
        slugs = models_param.split(',')

        if len(slugs) != 2:
            return Response({
                'success': False,
                'data': None,
                'message': '두 개의 제품 slug가 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_a = Product.objects.prefetch_related('specs', 'scores').get(slug=slugs[0], is_active=True)
            product_b = Product.objects.prefetch_related('specs', 'scores').get(slug=slugs[1], is_active=True)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': '제품을 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer_a = ProductDetailSerializer(product_a)
        serializer_b = ProductDetailSerializer(product_b)

        # TODO: 실제 투표 수 조회 로직 추가
        data = {
            'model_a': serializer_a.data,
            'model_b': serializer_b.data,
            'vote_a': 50,
            'vote_b': 50,
            'seo_meta': {
                'title': f"{product_a.name} vs {product_b.name} 비교 계급도 2026",
                'description': f"{product_a.name}과 {product_b.name} 스펙, 후기 비교 분석"
            }
        }

        return Response({
            'success': True,
            'data': data,
            'message': 'OK'
        })

    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """제품의 리뷰 목록 조회"""
        product = self.get_object()
        from reviews.serializers import ReviewSerializer

        reviews = product.reviews.filter(is_visible=True).select_related('user')

        # 나와 비슷한 사람 필터링
        width = request.query_params.get('width')
        pronation = request.query_params.get('pronation')

        if width:
            reviews = reviews.filter(user__profile__foot_width=width)
        if pronation:
            reviews = reviews.filter(user__profile__pronation=pronation)

        # 통계
        similar_count = reviews.count()
        repurchase_rate = 73  # TODO: 실제 재구매율 계산

        serializer = ReviewSerializer(reviews[:20], many=True)

        return Response({
            'success': True,
            'data': {
                'similar_user_stats': {
                    'total': similar_count,
                    'repurchase_rate': repurchase_rate,
                    'avg_size_fit': 'true'
                },
                'reviews': serializer.data
            },
            'message': 'OK'
        })


# 하위 호환성을 위한 별칭
ShoeModelViewSet = ProductViewSet
