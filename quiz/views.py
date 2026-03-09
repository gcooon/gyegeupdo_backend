from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import QuizSession
from .serializers import QuizInputSerializer, QuizResultSerializer
from brands.models import Category


class QuizViewSet(viewsets.ViewSet):
    """퀴즈 API ViewSet - 카테고리별 동적 퀴즈 지원"""

    def create(self, request):
        """퀴즈 제출 및 추천 결과 반환"""
        serializer = QuizInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_slug = serializer.validated_data.get('category', 'running-shoes')
        answers = serializer.validated_data.get('answers', {})
        budget_max = serializer.validated_data.get('budget_max')

        # 카테고리 조회
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': f'카테고리를 찾을 수 없습니다: {category_slug}'
            }, status=status.HTTP_404_NOT_FOUND)

        # 퀴즈 세션 생성
        session = QuizSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            category=category,
            answers=answers,
            budget_max=budget_max,
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
            session = QuizSession.objects.select_related('category').get(session_key=session_key)
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

    @action(detail=False, methods=['get'], url_path='questions/(?P<category_slug>[^/.]+)')
    def questions(self, request, category_slug=None):
        """카테고리별 퀴즈 질문 조회"""
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'message': f'카테고리를 찾을 수 없습니다: {category_slug}'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'data': {
                'category': {
                    'slug': category.slug,
                    'name': category.name,
                    'icon': category.icon,
                },
                'questions': category.quiz_definitions or []
            },
            'message': 'OK'
        })
