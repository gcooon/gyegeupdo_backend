from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models.functions import Substr, Coalesce
from django.db.models import Value
from .models import Product, ProductComment, ProductLike, Post, PostComment, PostLike
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    ProductCommentSerializer, ProductCommentCreateSerializer,
    PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer,
    PostCommentSerializer, PostCommentCreateSerializer
)


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 500


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
        # 조회수 증가
        instance.increment_view()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        """제품 좋아요 토글"""
        product = self.get_object()

        like, created = ProductLike.objects.get_or_create(product=product, user=request.user)

        if not created:
            # 이미 좋아요한 경우 취소
            like.delete()
            product.refresh_from_db()
            return Response({
                'success': True,
                'data': {'is_liked': False, 'like_count': product.like_count},
                'message': '좋아요가 취소되었습니다.'
            })

        # 좋아요 추가
        product.refresh_from_db()
        return Response({
            'success': True,
            'data': {'is_liked': True, 'like_count': product.like_count},
            'message': '좋아요!'
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

        # 좋아요 수 기반 비교 비율 계산
        likes_a = product_a.like_count or 0
        likes_b = product_b.like_count or 0
        total_likes = likes_a + likes_b
        data = {
            'model_a': serializer_a.data,
            'model_b': serializer_b.data,
            'vote_a': round(likes_a / total_likes * 100) if total_likes > 0 else 50,
            'vote_b': round(likes_b / total_likes * 100) if total_likes > 0 else 50,
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
        from django.db.models import Avg, Count
        stats = reviews.aggregate(
            total=Count('id'),
            avg_fit=Avg('fit_score'),
        )
        # 사이즈 핏 최빈값 계산
        size_fit_mode = reviews.values('size_fit').annotate(
            cnt=Count('id')
        ).order_by('-cnt').first()

        serializer = ReviewSerializer(reviews[:20], many=True)

        return Response({
            'success': True,
            'data': {
                'similar_user_stats': {
                    'total': stats['total'] or 0,
                    'avg_fit_score': round(stats['avg_fit'] or 0, 1),
                    'avg_size_fit': size_fit_mode['size_fit'] if size_fit_mode else 'true',
                },
                'reviews': serializer.data
            },
            'message': 'OK'
        })

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, slug=None):
        """제품 댓글 목록 조회 / 작성"""
        product = self.get_object()

        if request.method == 'GET':
            # 최상위 댓글만 조회 (대댓글은 replies로 포함)
            comments = product.comments.filter(parent=None).select_related(
                'user', 'user__profile'
            ).prefetch_related('replies', 'replies__user', 'replies__user__profile')

            # 페이지네이션
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
            offset = (page - 1) * limit

            total_count = comments.count()
            comments = comments.order_by('-created_at')[offset:offset + limit]

            serializer = ProductCommentSerializer(
                comments, many=True, context={'request': request}
            )

            return Response({
                'success': True,
                'data': {
                    'items': serializer.data,
                    'total_count': total_count,
                    'has_next': offset + limit < total_count
                },
                'message': 'OK'
            })

        # POST - 댓글 작성
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'data': None,
                'message': '로그인이 필요합니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductCommentCreateSerializer(
            data=request.data,
            context={'request': request, 'product': product}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response({
            'success': True,
            'data': ProductCommentSerializer(comment, context={'request': request}).data,
            'message': '댓글이 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)')
    def delete_comment(self, request, slug=None, comment_id=None):
        """제품 댓글 삭제"""
        product = self.get_object()

        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'data': None,
                'message': '로그인이 필요합니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = ProductComment.objects.get(id=comment_id, product=product)
        except ProductComment.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': '댓글을 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 작성자만 삭제 가능
        if comment.user != request.user:
            return Response({
                'success': False,
                'data': None,
                'message': '삭제 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({
            'success': True,
            'data': None,
            'message': '댓글이 삭제되었습니다.'
        })


# 하위 호환성을 위한 별칭
ShoeModelViewSet = ProductViewSet


class PostPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """게시판 API ViewSet"""
    queryset = Post.objects.select_related('user', 'user__profile', 'category')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return PostCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('product', 'product__brand')

        params = self.request.query_params

        # 카테고리 필터
        category = params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        # 태그 필터
        tag = params.get('tag')
        if tag:
            queryset = queryset.filter(tag=tag)

        # 제품 필터
        product = params.get('product')
        if product:
            queryset = queryset.filter(product__slug=product)

        # 검색
        search = params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_list_queryset(self):
        """
        목록 조회 전용 최적화 쿼리셋
        - only(): 필요한 필드만 명시적으로 로딩
        - content_preview를 DB 레벨에서 계산 (Substr)

        Note: defer('content') 대신 only() 사용
        - defer + Substr 조합 시 Django 버전별 동작 차이 가능성 회피
        - 명시적으로 필요한 필드만 로딩하여 더 안전
        """
        return self.get_queryset().only(
            'id', 'title', 'tag', 'rating', 'view_count', 'like_count',
            'comment_count', 'is_notice', 'created_at',
            # FK 필드 (select_related로 조인됨)
            'user', 'category', 'product',
        ).annotate(
            _content_preview=Coalesce(
                Substr('content', 1, 100),
                Value('')
            )
        )

    @method_decorator(cache_page(30))  # 30초 캐시 (글 작성 후 반영 지연 최소화)
    def list(self, request, *args, **kwargs):
        # 최적화된 쿼리셋 사용
        queryset = self.filter_queryset(self.get_list_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
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

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': {'count': len(serializer.data), 'results': serializer.data},
            'message': 'OK'
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 조회수 증가
        instance.increase_view_count()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        return Response({
            'success': True,
            'data': PostDetailSerializer(post, context={'request': request}).data,
            'message': '게시글이 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # 작성자만 수정 가능
        if instance.user != request.user:
            return Response({
                'success': False,
                'data': None,
                'message': '수정 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'data': PostDetailSerializer(instance, context={'request': request}).data,
            'message': '게시글이 수정되었습니다.'
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 작성자만 삭제 가능
        if instance.user != request.user:
            return Response({
                'success': False,
                'data': None,
                'message': '삭제 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response({
            'success': True,
            'data': None,
            'message': '게시글이 삭제되었습니다.'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """게시글 좋아요 토글"""
        post = self.get_object()

        like, created = PostLike.objects.get_or_create(post=post, user=request.user)

        if not created:
            # 이미 좋아요한 경우 취소
            like.delete()
            return Response({
                'success': True,
                'data': {'is_liked': False, 'like_count': post.like_count},
                'message': '좋아요가 취소되었습니다.'
            })

        # 좋아요 추가
        post.refresh_from_db()
        return Response({
            'success': True,
            'data': {'is_liked': True, 'like_count': post.like_count},
            'message': '좋아요!'
        })

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """게시글 댓글 목록 조회 / 작성"""
        post = self.get_object()

        if request.method == 'GET':
            comments = post.comments.filter(parent=None).select_related(
                'user', 'user__profile'
            ).prefetch_related('replies', 'replies__user', 'replies__user__profile')

            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
            offset = (page - 1) * limit

            total_count = comments.count()
            comments = comments.order_by('-created_at')[offset:offset + limit]

            serializer = PostCommentSerializer(
                comments, many=True, context={'request': request}
            )

            return Response({
                'success': True,
                'data': {
                    'items': serializer.data,
                    'total_count': total_count,
                    'has_next': offset + limit < total_count
                },
                'message': 'OK'
            })

        # POST
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'data': None,
                'message': '로그인이 필요합니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostCommentCreateSerializer(
            data=request.data,
            context={'request': request, 'post': post}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        # 댓글 수 갱신
        post.refresh_from_db()

        return Response({
            'success': True,
            'data': PostCommentSerializer(comment, context={'request': request}).data,
            'message': '댓글이 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)',
            permission_classes=[IsAuthenticated])
    def delete_comment(self, request, pk=None, comment_id=None):
        """게시글 댓글 삭제"""
        post = self.get_object()

        try:
            comment = PostComment.objects.get(id=comment_id, post=post)
        except PostComment.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': '댓글을 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 작성자 또는 게시글 작성자만 삭제 가능
        if comment.user != request.user and post.user != request.user:
            return Response({
                'success': False,
                'data': None,
                'message': '삭제 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({
            'success': True,
            'data': None,
            'message': '댓글이 삭제되었습니다.'
        })
