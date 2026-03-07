from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    계급도 카테고리 (러닝화, 치킨, 남자시계 등).
    각 카테고리는 자체적인 스펙 정의와 점수 정의를 가짐.
    """
    name = models.CharField(max_length=100, verbose_name='카테고리명')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='슬러그')
    icon = models.CharField(max_length=10, default='📦', verbose_name='아이콘')
    description = models.TextField(blank=True, verbose_name='설명')

    # 프론트엔드 표시 설정 (JSON)
    # 예: {"color": "#E94560", "heroTitle": "러닝화 계급도", ...}
    display_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='표시 설정',
        help_text='프론트엔드 표시 설정 (color, heroTitle, heroDescription 등)'
    )

    # 동적 스펙 정의 (JSON)
    spec_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='스펙 정의',
        help_text='카테고리별 스펙 필드 정의 (JSON 배열)'
    )

    # 동적 점수 정의 (JSON)
    score_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='점수 정의',
        help_text='카테고리별 점수 필드 정의 (JSON 배열)'
    )

    # 브랜드 티어 점수 가중치 정의 (JSON)
    brand_score_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='브랜드 점수 정의',
        help_text='브랜드 티어 점수 가중치 정의 (JSON 배열)'
    )

    # 퀴즈 질문 정의 (JSON)
    quiz_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='퀴즈 정의',
        help_text='카테고리별 퀴즈 질문 정의 (JSON 배열)'
    )

    # 용도/타입 선택지 정의 (JSON)
    filter_definitions = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='필터 정의',
        help_text='카테고리별 필터 선택지 정의 (JSON 객체)'
    )

    display_order = models.IntegerField(default=0, verbose_name='표시 순서')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """브랜드 정보 및 티어 점수."""
    TIER_CHOICES = [
        ('S', 'S티어'),
        ('A', 'A티어'),
        ('B', 'B티어'),
        ('C', 'C티어'),
        ('D', 'D티어'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='brands',
        verbose_name='카테고리'
    )
    name = models.CharField(max_length=100, verbose_name='브랜드명')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='슬러그')
    logo_url = models.URLField(blank=True, verbose_name='로고 URL')
    tier = models.CharField(max_length=1, choices=TIER_CHOICES, default='C', verbose_name='티어')
    tier_score = models.FloatField(default=0.0, verbose_name='티어 점수')

    # 레거시 고정 점수 필드 (러닝화 전용, 하위 호환)
    lineup_score = models.FloatField(default=0.0, verbose_name='라인업 점수')
    tech_score = models.FloatField(default=0.0, verbose_name='기술력 점수')
    durability_score = models.FloatField(default=0.0, verbose_name='내구성 점수')
    community_score = models.FloatField(default=0.0, verbose_name='커뮤니티 점수')

    description = models.TextField(blank=True, verbose_name='설명')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '브랜드'
        verbose_name_plural = '브랜드'
        ordering = ['-tier_score', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['tier']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.tier}티어)"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        # BrandScore가 있으면 동적 점수로 계산, 없으면 레거시 필드 사용
        super().save(*args, **kwargs)
        self._calculate_tier_score()

    def _calculate_tier_score(self):
        """BrandScore 기반 또는 레거시 필드 기반으로 티어 점수 계산"""
        brand_scores = self.scores.all()
        if brand_scores.exists():
            # 동적 점수 기반 계산
            definitions = self.category.brand_score_definitions or []
            weight_map = {d['key']: d.get('weight', 25) for d in definitions}
            total_weight = sum(weight_map.values()) or 100

            weighted_sum = 0
            for bs in brand_scores:
                weight = weight_map.get(bs.key, 25)
                weighted_sum += bs.value * weight

            new_score = weighted_sum / total_weight
        else:
            # 레거시 고정 필드 기반
            new_score = (
                self.lineup_score * 0.25 +
                self.tech_score * 0.30 +
                self.durability_score * 0.25 +
                self.community_score * 0.20
            )

        # 티어 자동 결정
        if new_score >= 85:
            new_tier = 'S'
        elif new_score >= 75:
            new_tier = 'A'
        elif new_score >= 60:
            new_tier = 'B'
        elif new_score >= 45:
            new_tier = 'C'
        else:
            new_tier = 'D'

        if self.tier_score != new_score or self.tier != new_tier:
            Brand.objects.filter(pk=self.pk).update(
                tier_score=new_score,
                tier=new_tier
            )
            self.tier_score = new_score
            self.tier = new_tier


class BrandScore(models.Model):
    """브랜드의 동적 점수 (카테고리별 다른 평가 항목 지원)"""
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='브랜드'
    )
    key = models.CharField(max_length=100, verbose_name='점수 키')
    label = models.CharField(max_length=100, blank=True, verbose_name='표시 이름')
    value = models.FloatField(default=0.0, verbose_name='점수 (0-100)')

    class Meta:
        verbose_name = '브랜드 점수'
        verbose_name_plural = '브랜드 점수'
        unique_together = ('brand', 'key')

    def __str__(self):
        return f"{self.brand.name} - {self.label or self.key}: {self.value}"

    def save(self, *args, **kwargs):
        # label이 비어있으면 카테고리 정의에서 가져오기
        if not self.label:
            definitions = self.brand.category.brand_score_definitions or []
            for d in definitions:
                if d['key'] == self.key:
                    self.label = d.get('label', self.key)
                    break
        super().save(*args, **kwargs)
        # 브랜드 티어 점수 재계산
        self.brand._calculate_tier_score()
