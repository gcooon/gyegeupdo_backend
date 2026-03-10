from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import TierDispute, DisputeVote, TrendLog, UserTierChart, TierChartComment, TierChartLike
from .serializers import (
    TierDisputeListSerializer,
    TierDisputeCreateSerializer,
    DisputeVoteSerializer,
    TrendLogSerializer,
    UserTierChartListSerializer,
    UserTierChartDetailSerializer,
    UserTierChartCreateSerializer,
    UserTierChartUpdateSerializer,
    TierChartCommentSerializer,
    TierChartCommentCreateSerializer
)


class TierDisputeViewSet(viewsets.ModelViewSet):
    """이의제기 API ViewSet"""
    queryset = TierDispute.objects.select_related('product', 'user')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return TierDisputeCreateSerializer
        return TierDisputeListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-support_count', '-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'success': True,
            'data': TierDisputeListSerializer(serializer.instance).data,
            'message': '이의제기가 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """투표하기"""
        dispute = self.get_object()

        # 이미 투표했는지 확인
        if DisputeVote.objects.filter(dispute=dispute, user=request.user).exists():
            return Response({
                'success': False,
                'data': None,
                'message': '이미 투표하셨습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = DisputeVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        DisputeVote.objects.create(
            dispute=dispute,
            user=request.user,
            vote=serializer.validated_data['vote']
        )

        return Response({
            'success': True,
            'data': {
                'support_count': dispute.support_count,
                'oppose_count': dispute.oppose_count
            },
            'message': '투표가 완료되었습니다.'
        })


class TrendViewSet(viewsets.ReadOnlyModelViewSet):
    """트렌드 API ViewSet"""
    queryset = TrendLog.objects.select_related('product', 'product__brand')
    serializer_class = TrendLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        period = self.request.query_params.get('period', 'weekly')
        direction = self.request.query_params.get('direction', 'up')
        limit = int(self.request.query_params.get('limit', 5))

        queryset = queryset.filter(period=period, trend=direction)
        queryset = queryset.order_by('-score' if direction == 'up' else 'score')

        return queryset[:limit]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })


class UserTierChartViewSet(viewsets.ModelViewSet):
    """사용자 계급도 API ViewSet"""
    queryset = UserTierChart.objects.select_related('user', 'user__profile')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'create':
            return UserTierChartCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserTierChartUpdateSerializer
        elif self.action == 'retrieve':
            return UserTierChartDetailSerializer
        return UserTierChartListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # 목록에서는 공개 계급도만 (본인 것은 포함)
        if self.action == 'list':
            if user.is_authenticated:
                queryset = queryset.filter(
                    Q(visibility='public') | Q(user=user)
                )
            else:
                queryset = queryset.filter(visibility='public')

        # 정렬 옵션
        sort = self.request.query_params.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.order_by('-like_count', '-view_count', '-created_at')
        elif sort == 'views':
            queryset = queryset.order_by('-view_count', '-created_at')
        else:  # latest
            queryset = queryset.order_by('-created_at')

        # 검색
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # 추천 필터
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        # 사용자 필터
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # 페이지네이션
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 12))
        offset = (page - 1) * limit

        total_count = queryset.count()
        queryset = queryset[offset:offset + limit]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'items': serializer.data,
                'total_count': total_count,
                'page': page,
                'limit': limit,
                'has_next': offset + limit < total_count
            },
            'message': 'OK'
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 비공개 체크
        if instance.visibility == 'private':
            if not request.user.is_authenticated or instance.user != request.user:
                return Response({
                    'success': False,
                    'data': None,
                    'message': '비공개 계급도입니다.'
                }, status=status.HTTP_403_FORBIDDEN)

        # 조회수 증가 (본인 제외)
        if not request.user.is_authenticated or instance.user != request.user:
            instance.increment_view()

        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            'success': True,
            'data': UserTierChartDetailSerializer(instance, context={'request': request}).data,
            'message': '계급도가 생성되었습니다.'
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # 본인만 수정 가능
        if instance.user != request.user:
            return Response({
                'success': False,
                'data': None,
                'message': '수정 권한이 없습니다.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            'success': True,
            'data': UserTierChartDetailSerializer(instance, context={'request': request}).data,
            'message': '계급도가 수정되었습니다.'
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 본인만 삭제 가능
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
            'message': '계급도가 삭제되었습니다.'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        """좋아요 토글"""
        instance = self.get_object()

        like, created = TierChartLike.objects.get_or_create(
            tier_chart=instance,
            user=request.user
        )

        if not created:
            # 이미 좋아요 -> 취소
            like.delete()
            instance.refresh_from_db(fields=['like_count'])
            return Response({
                'success': True,
                'data': {
                    'is_liked': False,
                    'like_count': instance.like_count
                },
                'message': '좋아요가 취소되었습니다.'
            })

        instance.refresh_from_db(fields=['like_count'])
        return Response({
            'success': True,
            'data': {
                'is_liked': True,
                'like_count': instance.like_count
            },
            'message': '좋아요!'
        })

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, slug=None):
        """댓글 목록 조회 / 작성"""
        instance = self.get_object()

        if request.method == 'GET':
            # 댓글 목록
            comments = instance.comments.filter(parent=None).order_by('-created_at')

            # 페이지네이션
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
            offset = (page - 1) * limit

            total_count = comments.count()
            comments = comments[offset:offset + limit]

            serializer = TierChartCommentSerializer(
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

        serializer = TierChartCommentCreateSerializer(
            data=request.data,
            context={'request': request, 'tier_chart': instance}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response({
            'success': True,
            'data': TierChartCommentSerializer(comment, context={'request': request}).data,
            'message': '댓글이 등록되었습니다.'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)')
    def delete_comment(self, request, slug=None, comment_id=None):
        """댓글 삭제"""
        instance = self.get_object()

        try:
            comment = TierChartComment.objects.get(
                id=comment_id,
                tier_chart=instance
            )
        except TierChartComment.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': '댓글을 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 본인 또는 계급도 작성자만 삭제 가능
        if comment.user != request.user and instance.user != request.user:
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_charts(self, request):
        """내 계급도 목록"""
        queryset = self.get_queryset().filter(user=request.user).order_by('-created_at')

        serializer = UserTierChartListSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    # ===== 승격 시스템 API =====

    @action(detail=False, methods=['get'])
    def promotion_candidates(self, request):
        """승급 후보 목록 조회 (100점 이상)"""
        queryset = self.get_queryset().filter(
            visibility='public',
            promotion_status__in=['rising', 'candidate']
        ).order_by('-like_count', '-view_count', '-created_at')

        # 페이지네이션
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        offset = (page - 1) * limit

        total_count = queryset.count()
        queryset = queryset[offset:offset + limit]

        serializer = UserTierChartListSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response({
            'success': True,
            'data': {
                'items': serializer.data,
                'total_count': total_count,
                'page': page,
                'limit': limit,
                'has_next': offset + limit < total_count
            },
            'message': 'OK'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def promote(self, request, slug=None):
        """계급도 승급 처리 (관리자 전용)"""
        instance = self.get_object()

        if instance.promotion_status == 'promoted':
            return Response({
                'success': False,
                'data': None,
                'message': '이미 승급된 계급도입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.promotion_status = 'promoted'
        instance.promoted_at = timezone.now()
        instance.promoted_by = request.user
        instance.save(update_fields=['promotion_status', 'promoted_at', 'promoted_by'])

        serializer = UserTierChartDetailSerializer(instance, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f'"{instance.title}" 계급도가 승급 처리되었습니다.'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def demote(self, request, slug=None):
        """계급도 승급 취소 (관리자 전용)"""
        instance = self.get_object()

        if instance.promotion_status == 'normal':
            return Response({
                'success': False,
                'data': None,
                'message': '일반 상태의 계급도입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 점수 기반으로 상태 재계산
        instance.promotion_status = 'normal'
        instance.promoted_at = None
        instance.promoted_by = None
        instance.save(update_fields=['promotion_status', 'promoted_at', 'promoted_by'])

        # 점수 기반 상태 재설정
        instance.update_promotion_status()
        instance.refresh_from_db()

        serializer = UserTierChartDetailSerializer(instance, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f'"{instance.title}" 계급도의 승급이 취소되었습니다.'
        })
