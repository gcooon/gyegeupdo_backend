from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import QuizSession
from .serializers import QuizInputSerializer, QuizResultSerializer


class QuizViewSet(viewsets.ViewSet):
    """퀴즈 API ViewSet"""

    def create(self, request):
        """퀴즈 제출 및 추천 결과 반환"""
        serializer = QuizInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 퀴즈 세션 생성
        session = QuizSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            foot_width=serializer.validated_data['foot_width'],
            pronation=serializer.validated_data['pronation'],
            usage_type=serializer.validated_data['usage_type'],
            budget_max=serializer.validated_data['budget_max'],
            priority=serializer.validated_data['priority']
        )

        result_serializer = QuizResultSerializer(session)

        return Response({
            'success': True,
            'data': result_serializer.data,
            'message': 'OK'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='result/(?P<session_key>[^/.]+)')
    def result(self, request, session_key=None):
        """퀴즈 결과 조회"""
        try:
            session = QuizSession.objects.get(session_key=session_key)
        except QuizSession.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': '결과를 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizResultSerializer(session)

        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'OK'
        })
