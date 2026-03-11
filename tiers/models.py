from django.db import models
from django.db.models import F
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
            # 투표 수 업데이트 (F expression으로 race condition 방지)
            if self.vote == 'support':
                TierDispute.objects.filter(pk=self.dispute_id).update(
                    support_count=F('support_count') + 1
                )
            else:
                TierDispute.objects.filter(pk=self.dispute_id).update(
                    oppose_count=F('oppose_count') + 1
                )
            self.dispute.refresh_from_db()
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

    PROMOTION_STATUS_CHOICES = [
        ('normal', '일반'),
        ('rising', '급상승'),
        ('candidate', '승급 후보'),
        ('promoted', '승급됨'),  # HOT 노출 (7일)
        ('hall_of_fame', '명예의 전당'),  # 영구 노출
    ]

    LANGUAGE_CHOICES = [
        ('ko', '한국어'),
        ('en', 'English'),
        ('ja', '日本語'),
        ('zh', '中文'),
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

    # 승격 시스템
    promotion_status = models.CharField(
        max_length=20,
        choices=PROMOTION_STATUS_CHOICES,
        default='normal',
        verbose_name='승격 상태'
    )
    promoted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='승격일'
    )
    promoted_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='promoted_tier_charts',
        verbose_name='승격 처리자'
    )

    # HOT 노출 기간 (promoted 상태일 때)
    hot_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='HOT 노출 종료일',
        help_text='이 날짜까지 홈페이지 HOT 섹션에 노출'
    )

    # 명예의 전당
    hall_of_fame_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='명예의 전당 등록일'
    )

    # 공식 계급도 전환 추적
    converted_to_official = models.BooleanField(
        default=False,
        verbose_name='공식 계급도 전환 여부'
    )
    converted_category_slug = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='전환된 카테고리 슬러그',
        help_text='공식 계급도로 전환된 경우 해당 카테고리 슬러그'
    )

    # 국제화 필드
    language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='ko',
        verbose_name='언어'
    )
    author_country = models.CharField(
        max_length=2,
        blank=True,
        default='',
        verbose_name='작성자 국가',
        help_text='ISO 3166-1 alpha-2 (KR, US, JP...)'
    )
    is_global = models.BooleanField(
        default=True,
        verbose_name='글로벌 노출',
        help_text='False면 해당 언어권에서만 노출'
    )

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
            models.Index(fields=['promotion_status', '-created_at']),
            models.Index(fields=['language', '-created_at']),
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
        """조회수 증가 (F expression으로 race condition 방지)"""
        UserTierChart.objects.filter(pk=self.pk).update(
            view_count=F('view_count') + 1
        )
        self.refresh_from_db(fields=['view_count'])

    @property
    def promotion_score(self) -> float:
        """승격 점수 계산: (좋아요 × 3) + (조회수 × 0.1) + (댓글수 × 5)"""
        return (self.like_count * 3) + (self.view_count * 0.1) + (self.comment_count * 5)

    @property
    def promotion_progress(self) -> dict:
        """승격 진행률 및 상태 정보 반환"""
        score = self.promotion_score

        # 명예의 전당
        if self.promotion_status == 'hall_of_fame':
            return {
                'current_score': score,
                'target_score': None,
                'progress_percent': 100,
                'status': 'hall_of_fame',
                'status_display': '명예의 전당',
                'score_breakdown': {
                    'likes': self.like_count * 3,
                    'views': self.view_count * 0.1,
                    'comments': self.comment_count * 5,
                }
            }

        # HOT 노출 중
        if self.promotion_status == 'promoted':
            return {
                'current_score': score,
                'target_score': None,
                'progress_percent': 100,
                'status': 'promoted',
                'status_display': 'HOT',
                'hot_until': self.hot_until,
                'score_breakdown': {
                    'likes': self.like_count * 3,
                    'views': self.view_count * 0.1,
                    'comments': self.comment_count * 5,
                }
            }

        # 점수 기반 상태 결정
        if score >= 100:
            status = 'candidate'
            status_display = '승급 후보'
            target_score = None
            progress_percent = 100
        elif score >= 50:
            status = 'rising'
            status_display = '급상승'
            target_score = 100
            progress_percent = min(((score - 50) / 50) * 100, 100)
        else:
            status = 'normal'
            status_display = '일반'
            target_score = 50
            progress_percent = min((score / 50) * 100, 100)

        return {
            'current_score': score,
            'target_score': target_score,
            'progress_percent': round(progress_percent, 1),
            'status': status,
            'status_display': status_display,
            'score_breakdown': {
                'likes': self.like_count * 3,
                'views': round(self.view_count * 0.1, 1),
                'comments': self.comment_count * 5,
            }
        }

    def update_promotion_status(self):
        """점수 기반 승격 상태 자동 업데이트 (promoted, hall_of_fame 제외)"""
        if self.promotion_status in ('promoted', 'hall_of_fame'):
            return  # 이미 승급된 경우 변경하지 않음

        score = self.promotion_score
        if score >= 100:
            new_status = 'candidate'
        elif score >= 50:
            new_status = 'rising'
        else:
            new_status = 'normal'

        if self.promotion_status != new_status:
            self.promotion_status = new_status
            self.save(update_fields=['promotion_status'])

    def promote_to_hot(self, promoted_by_user, days=7):
        """HOT 계급도로 승급 (홈페이지 노출)"""
        from django.utils import timezone
        from datetime import timedelta

        self.promotion_status = 'promoted'
        self.promoted_at = timezone.now()
        self.promoted_by = promoted_by_user
        self.hot_until = timezone.now() + timedelta(days=days)
        self.is_featured = True
        self.save(update_fields=[
            'promotion_status', 'promoted_at', 'promoted_by',
            'hot_until', 'is_featured'
        ])

    def promote_to_hall_of_fame(self, promoted_by_user=None):
        """명예의 전당으로 승급"""
        from django.utils import timezone

        self.promotion_status = 'hall_of_fame'
        self.hall_of_fame_at = timezone.now()
        if promoted_by_user:
            self.promoted_by = promoted_by_user
        self.is_featured = True
        self.save(update_fields=[
            'promotion_status', 'hall_of_fame_at', 'promoted_by', 'is_featured'
        ])

    def check_hot_expiry(self):
        """HOT 기간 만료 체크 및 명예의 전당 자동 전환"""
        from django.utils import timezone

        if self.promotion_status == 'promoted' and self.hot_until:
            if timezone.now() > self.hot_until:
                self.promote_to_hall_of_fame()


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
            # 댓글 수 업데이트 (F expression으로 race condition 방지)
            UserTierChart.objects.filter(pk=self.tier_chart_id).update(
                comment_count=F('comment_count') + 1
            )
            # 승격 상태 자동 업데이트
            self.tier_chart.refresh_from_db()
            self.tier_chart.update_promotion_status()

    def delete(self, *args, **kwargs):
        tier_chart_id = self.tier_chart_id
        tier_chart = self.tier_chart
        super().delete(*args, **kwargs)
        # 댓글 수 업데이트 (F expression으로 race condition 방지)
        UserTierChart.objects.filter(pk=tier_chart_id).update(
            comment_count=F('comment_count') - 1
        )
        # 승격 상태 자동 업데이트
        tier_chart.refresh_from_db()
        tier_chart.update_promotion_status()


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
            # 좋아요 수 업데이트 (F expression으로 race condition 방지)
            UserTierChart.objects.filter(pk=self.tier_chart_id).update(
                like_count=F('like_count') + 1
            )
            # 승격 상태 자동 업데이트
            self.tier_chart.refresh_from_db()
            self.tier_chart.update_promotion_status()

    def delete(self, *args, **kwargs):
        tier_chart_id = self.tier_chart_id
        tier_chart = self.tier_chart
        super().delete(*args, **kwargs)
        # 좋아요 수 업데이트 (F expression으로 race condition 방지)
        UserTierChart.objects.filter(pk=tier_chart_id).update(
            like_count=F('like_count') - 1
        )
        # 승격 상태 자동 업데이트
        tier_chart.refresh_from_db()
        tier_chart.update_promotion_status()
