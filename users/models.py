from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    """User 테이블과 1:1 관계. 발형/성향 정보를 저장."""
    FOOT_WIDTH_CHOICES = [
        ('narrow', '좁음'),
        ('normal', '보통'),
        ('wide', '넓음'),
        ('extra_wide', '매우 넓음'),
    ]
    PRONATION_CHOICES = [
        ('overpronation', '과내전'),
        ('neutral', '중립'),
        ('supination', '과외전'),
    ]
    USAGE_TYPE_CHOICES = [
        ('beginner', '입문자'),
        ('daily', '데일리'),
        ('tempo', '템포'),
        ('race', '레이스'),
    ]
    PRIORITY_CHOICES = [
        ('cushion', '쿠션'),
        ('speed', '속도'),
        ('design', '디자인'),
    ]
    BADGE_CHOICES = [
        ('none', '일반'),
        ('verified', '검증러너'),
        ('reviewer', '리뷰어'),
        ('master', '마스터'),
        ('pioneer', '파이오니어'),
    ]
    LANGUAGE_CHOICES = [
        ('ko', '한국어'),
        ('en', 'English'),
        ('ja', '日本語'),
        ('zh', '中文'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='사용자'
    )
    foot_width = models.CharField(
        max_length=20,
        choices=FOOT_WIDTH_CHOICES,
        default='normal',
        verbose_name='발볼'
    )
    pronation = models.CharField(
        max_length=20,
        choices=PRONATION_CHOICES,
        default='neutral',
        verbose_name='발 유형'
    )
    usage_type = models.CharField(
        max_length=20,
        choices=USAGE_TYPE_CHOICES,
        default='daily',
        verbose_name='주 용도'
    )
    budget_min = models.IntegerField(default=0, verbose_name='예산 최소')
    budget_max = models.IntegerField(default=300000, verbose_name='예산 최대')
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='cushion',
        verbose_name='우선순위'
    )
    total_km = models.IntegerField(default=0, verbose_name='총 주행거리')
    strava_proof_url = models.URLField(blank=True, verbose_name='스트라바 인증 URL')
    badge = models.CharField(
        max_length=20,
        choices=BADGE_CHOICES,
        default='none',
        verbose_name='배지'
    )
    review_weight = models.FloatField(default=1.0, verbose_name='리뷰 가중치')
    review_count = models.IntegerField(default=0, verbose_name='리뷰 수')
    dispute_accepted_count = models.IntegerField(default=0, verbose_name='채택된 이의제기 수')

    # 국제화 설정
    preferred_language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='ko',
        verbose_name='선호 언어'
    )
    country = models.CharField(
        max_length=2,
        blank=True,
        default='',
        verbose_name='국가',
        help_text='ISO 3166-1 alpha-2 (KR, US, JP...)'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필'

    def __str__(self):
        return f"{self.user.email}의 프로필"

    def update_badge(self):
        """배지 자동 업데이트"""
        if self.dispute_accepted_count >= 10:
            self.badge = 'pioneer'
            self.review_weight = 2.0
        elif self.review_count >= 50 and self.total_km >= 1000:
            self.badge = 'master'
            self.review_weight = 1.8
        elif self.review_count >= 20:
            self.badge = 'reviewer'
            self.review_weight = 1.5
        elif self.review_count >= 5 and self.total_km >= 100:
            self.badge = 'verified'
            self.review_weight = 1.3
        else:
            self.badge = 'none'
            self.review_weight = 1.0
        self.save()
