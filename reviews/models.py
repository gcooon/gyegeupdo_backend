from django.db import models
from django.contrib.auth import get_user_model
from models_app.models import Product

User = get_user_model()


class Review(models.Model):
    """체크박스형 리뷰. 별점 대신 항목별 점수로 데이터 구조화."""
    WIDTH_SCORE_CHOICES = [
        ('narrow', '좁음'),
        ('normal', '적당함'),
        ('wide', '넓음'),
    ]
    SIZE_FIT_CHOICES = [
        ('half_up', '반 사이즈 업'),
        ('true', '정사이즈'),
        ('half_down', '반 사이즈 다운'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='제품'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='작성자'
    )
    fit_score = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='착화감 점수'
    )
    width_score = models.CharField(
        max_length=20,
        choices=WIDTH_SCORE_CHOICES,
        verbose_name='발볼 평가'
    )
    size_fit = models.CharField(
        max_length=20,
        choices=SIZE_FIT_CHOICES,
        verbose_name='사이즈 핏'
    )
    usage_fit = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='용도 적합성'
    )
    pain_level = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 6)],
        default=0,
        verbose_name='통증 레벨'
    )
    durability_score = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='내구성 점수'
    )
    comment = models.TextField(blank=True, verbose_name='코멘트')
    proof_image_url = models.URLField(blank=True, verbose_name='인증 이미지 URL')
    running_km_at_review = models.IntegerField(default=0, verbose_name='작성 시점 주행거리')
    weight_multiplier = models.FloatField(default=1.0, verbose_name='가중치')
    is_visible = models.BooleanField(default=True, verbose_name='공개')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.email}의 {self.product.name} 리뷰"

    def save(self, *args, **kwargs):
        # 사용자 배지에 따른 가중치 적용
        if hasattr(self.user, 'profile'):
            self.weight_multiplier = self.user.profile.review_weight
        super().save(*args, **kwargs)
