from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Brand
from .serializers import CategorySerializer, BrandListSerializer, BrandDetailSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """카테고리 API ViewSet"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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
