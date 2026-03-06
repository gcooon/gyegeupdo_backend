from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, BadgeProgressSerializer, RegisterSerializer


class RegisterView(APIView):
    """회원가입 API"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                'message': '회원가입이 완료되었습니다.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'data': None,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    """사용자 API ViewSet"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """현재 로그인한 사용자 정보"""
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })

    @action(detail=False, methods=['get'], url_path='me/badge-progress')
    def badge_progress(self, request):
        """배지 진행률 조회"""
        profile = getattr(request.user, 'profile', None)

        if not profile:
            # 프로필이 없으면 생성
            profile = UserProfile.objects.create(user=request.user)

        # 다음 배지 결정
        badge_requirements = {
            'none': {'next': 'verified', 'review_required': 5, 'km_required': 100},
            'verified': {'next': 'reviewer', 'review_required': 20, 'km_required': 500},
            'reviewer': {'next': 'master', 'review_required': 50, 'km_required': 1000},
            'master': {'next': 'pioneer', 'review_required': 100, 'km_required': 5000},
            'pioneer': {'next': 'pioneer', 'review_required': 100, 'km_required': 5000},
        }

        current_req = badge_requirements.get(profile.badge, badge_requirements['none'])

        data = {
            'current_badge': profile.badge,
            'next_badge': current_req['next'],
            'progress': {
                'review_count': profile.review_count,
                'review_required': current_req['review_required'],
                'km': profile.total_km,
                'km_required': current_req['km_required']
            }
        }

        return Response({
            'success': True,
            'data': data,
            'message': 'OK'
        })

    @action(detail=False, methods=['patch'], url_path='me/profile')
    def update_profile(self, request):
        """프로필 업데이트"""
        profile = getattr(request.user, 'profile', None)

        if not profile:
            profile = UserProfile.objects.create(user=request.user)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data,
            'message': '프로필이 업데이트되었습니다.'
        })
