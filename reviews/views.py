from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """리뷰 API ViewSet"""
    queryset = Review.objects.filter(is_visible=True).select_related('user', 'product')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })
