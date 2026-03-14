from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReviewViewSet(viewsets.ModelViewSet):
    """리뷰 API ViewSet"""
    queryset = Review.objects.filter(is_visible=True).select_related('user', 'product')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response({
                'success': False,
                'data': None,
                'message': '이미 이 제품에 리뷰를 작성하셨습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 프로필 리뷰 수 업데이트
        if hasattr(request.user, 'profile'):
            request.user.profile.review_count += 1
            request.user.profile.update_badge()

        return Response({
            'success': True,
            'data': ReviewSerializer(serializer.instance).data,
            'message': '리뷰가 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

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
                    'previous': paginated_response.data['previous'],
                },
                'message': 'OK'
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {'count': len(serializer.data), 'results': serializer.data},
            'message': 'OK'
        })
