from django.db import models
from django.contrib.auth import get_user_model
from brands.models import Category
import uuid

User = get_user_model()


class QuizSession(models.Model):
    """퀴즈 세션 및 추천 결과. 카테고리별 동적 질문/답변 지원."""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quiz_sessions',
        verbose_name='사용자'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='quiz_sessions',
        verbose_name='카테고리'
    )
    session_key = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        verbose_name='세션 키'
    )
    answers = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='퀴즈 답변 (카테고리 quiz_definitions 기반)'
    )
    budget_max = models.IntegerField(null=True, blank=True, verbose_name='예산 최대')
    recommended_products = models.JSONField(
        default=list,
        blank=True,
        verbose_name='추천 제품 ID 목록'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '퀴즈 세션'
        verbose_name_plural = '퀴즈 세션'
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"{self.user.email}의 퀴즈 ({self.session_key[:8]})"
        return f"비회원 퀴즈 ({self.session_key[:8]})"

    def get_share_url(self):
        return f"/quiz/result/{self.session_key}"
