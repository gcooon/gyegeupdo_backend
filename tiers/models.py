from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()

# Product import는 선택적으로 (순환 참조 방지)
try:
    from models_app.models import Product
except ImportError:
    Product = None


class TierDispute(models.Model):
    """이의제기 시스템. support_count >= 30이면 status를 'colosseum'으로 변경."""
    DISPUTE_TYPE_CHOICES = [
        ('upgrade', '승급'),
        ('downgrade', '강등'),
    ]
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('colosseum', '콜로세움'),
        ('resolved', '해결됨'),
        ('rejected', '거절됨'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='disputes',
        verbose_name='제품'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disputes',
        verbose_name='제출자'
    )
    dispute_type = models.CharField(
        max_length=20,
        choices=DISPUTE_TYPE_CHOICES,
        verbose_name='이의제기 유형'
    )
    reason = models.TextField(verbose_name='사유')
    evidence_url = models.URLField(blank=True, verbose_name='증거 URL')
    support_count = models.IntegerField(default=0, verbose_name='찬성 수')
    oppose_count = models.IntegerField(default=0, verbose_name='반대 수')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='상태'
    )
    resolution = models.TextField(blank=True, verbose_name='결과')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='해결일')

    class Meta:
        verbose_name = '티어 이의제기'
        verbose_name_plural = '티어 이의제기'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'support_count']),
        ]

    def __str__(self):
        return f"{self.product.name} {self.get_dispute_type_display()} 요청"

    def update_status(self):
        """찬성 수에 따라 상태 자동 업데이트"""
        if self.support_count >= 30 and self.status == 'pending':
            self.status = 'colosseum'
            self.save()


class DisputeVote(models.Model):
    """이의제기 투표."""
    VOTE_CHOICES = [
        ('support', '찬성'),
        ('oppose', '반대'),
    ]

    dispute = models.ForeignKey(
        TierDispute,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='이의제기'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dispute_votes',
        verbose_name='투표자'
    )
    vote = models.CharField(
        max_length=10,
        choices=VOTE_CHOICES,
        verbose_name='투표'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='투표일')

    class Meta:
        verbose_name = '이의제기 투표'
        verbose_name_plural = '이의제기 투표'
        unique_together = ['dispute', 'user']

    def __str__(self):
        return f"{self.user.email}의 {self.get_vote_display()}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # 투표 수 업데이트
            if self.vote == 'support':
                self.dispute.support_count += 1
            else:
                self.dispute.oppose_count += 1
            self.dispute.save()
            self.dispute.update_status()


class TrendLog(models.Model):
    """주간/월간 트렌드 점수 기록."""
    PERIOD_CHOICES = [
        ('weekly', '주간'),
        ('monthly', '월간'),
    ]
    TREND_CHOICES = [
        ('up', '상승'),
        ('down', '하락'),
        ('stable', '유지'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='trend_logs',
        verbose_name='제품'
    )
    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        verbose_name='기간'
    )
    score = models.FloatField(verbose_name='점수')
    prev_score = models.FloatField(default=0.0, verbose_name='이전 점수')
    trend = models.CharField(
        max_length=10,
        choices=TREND_CHOICES,
        default='stable',
        verbose_name='추세'
    )
    rank = models.IntegerField(default=0, verbose_name='순위')
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='기록일')

    class Meta:
        verbose_name = '트렌드 로그'
        verbose_name_plural = '트렌드 로그'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['product', 'period', 'recorded_at']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.get_period_display()} ({self.get_trend_display()})"

    @property
    def score_change(self):
        return self.score - self.prev_score

    def save(self, *args, **kwargs):
        # 트렌드 자동 계산
        diff = self.score - self.prev_score
        if diff > 2:
            self.trend = 'up'
        elif diff < -2:
            self.trend = 'down'
        else:
            self.trend = 'stable'
        super().save(*args, **kwargs)


class UserTierChart(models.Model):
    """사용자가 만든 계급도"""
    VISIBILITY_CHOICES = [
        ('public', '공개'),
        ('private', '비공개'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tier_charts',
        verbose_name='작성자'
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, verbose_name='제목')
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='설명')

    # 티어 데이터 (JSON 형식)
    # {"S": [{"name": "아이템1", "reason": "이유"}, ...], "A": [...], ...}
    tier_data = models.JSONField(default=dict, verbose_name='티어 데이터')

    # 통계
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    comment_count = models.IntegerField(default=0, verbose_name='댓글 수')

    # 상태
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='public',
        verbose_name='공개 상태'
    )
    is_featured = models.BooleanField(default=False, verbose_name='추천 여부')

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자 계급도'
        verbose_name_plural = '사용자 계급도'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['visibility', '-like_count']),
            models.Index(fields=['-view_count']),
        ]

    def __str__(self):
        return f"{self.title} by {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            if not base_slug:
                base_slug = str(self.uuid)[:8]
            # 유니크 슬러그 생성
            slug = base_slug
            counter = 1
            while UserTierChart.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def share_url(self):
        """공유 URL"""
        return f"/my-tier/{self.slug}"

    def increment_view(self):
        """조회수 증가"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class TierChartComment(models.Model):
    """계급도 댓글"""
    tier_chart = models.ForeignKey(
        UserTierChart,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='계급도'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tier_chart_comments',
        verbose_name='작성자'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='상위 댓글'
    )
    content = models.TextField(max_length=1000, verbose_name='내용')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '계급도 댓글'
        verbose_name_plural = '계급도 댓글'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}: {self.content[:30]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # 댓글 수 업데이트
            self.tier_chart.comment_count = self.tier_chart.comments.count()
            self.tier_chart.save(update_fields=['comment_count'])

    def delete(self, *args, **kwargs):
        tier_chart = self.tier_chart
        super().delete(*args, **kwargs)
        # 댓글 수 업데이트
        tier_chart.comment_count = tier_chart.comments.count()
        tier_chart.save(update_fields=['comment_count'])


class TierChartLike(models.Model):
    """계급도 좋아요"""
    tier_chart = models.ForeignKey(
        UserTierChart,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='계급도'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tier_chart_likes',
        verbose_name='사용자'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '계급도 좋아요'
        verbose_name_plural = '계급도 좋아요'
        unique_together = ['tier_chart', 'user']

    def __str__(self):
        return f"{self.user.email} likes {self.tier_chart.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # 좋아요 수 업데이트
            self.tier_chart.like_count += 1
            self.tier_chart.save(update_fields=['like_count'])

    def delete(self, *args, **kwargs):
        tier_chart = self.tier_chart
        super().delete(*args, **kwargs)
        # 좋아요 수 업데이트
        tier_chart.like_count = tier_chart.likes.count()
        tier_chart.save(update_fields=['like_count'])
