from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    계급도 카테고리 (러닝화, 패딩, 치킨 등).
    각 카테고리는 자체적인 스펙 정의와 점수 정의를 가짐.
    """
    name = models.CharField(max_length=100, verbose_name='카테고리명')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='슬러그')
    icon = models.CharField(max_length=10, default='📦', verbose_name='아이콘')
    description = models.TextField(blank=True, verbose_name='설명')

    # 동적 스펙 정의 (JSON)
    # 예: [{"key": "drop_mm", "label": "드롭", "unit": "mm", "type": "number"},
    #      {"key": "weight_g", "label": "무게", "unit": "g", "type": "number"}]
    spec_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='스펙 정의',
        help_text='카테고리별 스펙 필드 정의 (JSON 배열)'
    )

    # 동적 점수 정의 (JSON)
    # 예: [{"key": "cushion_score", "label": "쿠션", "weight": 0.25},
    #      {"key": "durability_score", "label": "내구성", "weight": 0.25}]
    score_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='점수 정의',
        help_text='카테고리별 점수 필드 정의 (JSON 배열)'
    )

    # 브랜드 티어 점수 가중치 정의 (JSON)
    # 예: [{"key": "lineup_score", "label": "라인업", "weight": 0.25}, ...]
    brand_score_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='브랜드 점수 정의',
        help_text='브랜드 티어 점수 가중치 정의 (JSON 배열)'
    )

    # 퀴즈 질문 정의 (JSON)
    # 예: [{"id": "foot_width", "title": "발볼 넓이", "options": [...]}]
    quiz_definitions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='퀴즈 정의',
        help_text='카테고리별 퀴즈 질문 정의 (JSON 배열)'
    )

    # 용도/타입 선택지 정의 (JSON)
    # 예: {"usage": [{"value": "daily", "label": "데일리"}],
    #      "type": [{"value": "cushion", "label": "쿠션"}]}
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

    def get_default_spec_definitions(self):
        """러닝화 기본 스펙 정의 반환 (마이그레이션 용)"""
        return [
            {"key": "drop_mm", "label": "드롭", "unit": "mm", "type": "number"},
            {"key": "stack_mm", "label": "스택", "unit": "mm", "type": "number"},
            {"key": "weight_g", "label": "무게", "unit": "g", "type": "number"},
            {"key": "width", "label": "발볼", "unit": "", "type": "choice",
             "choices": [
                 {"value": "narrow", "label": "좁음"},
                 {"value": "normal", "label": "보통"},
                 {"value": "wide", "label": "넓음"},
                 {"value": "extra_wide", "label": "매우 넓음"}
             ]},
        ]

    def get_default_score_definitions(self):
        """러닝화 기본 점수 정의 반환 (마이그레이션 용)"""
        return [
            {"key": "cushion_score", "label": "쿠션", "weight": 0.20},
            {"key": "responsiveness_score", "label": "반발력", "weight": 0.20},
            {"key": "stability_score", "label": "안정성", "weight": 0.20},
            {"key": "durability_score", "label": "내구성", "weight": 0.20},
            {"key": "value_score", "label": "가성비", "weight": 0.20},
        ]


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
        # 티어 점수 자동 계산 (4개 점수의 가중 평균)
        self.tier_score = (
            self.lineup_score * 0.25 +
            self.tech_score * 0.30 +
            self.durability_score * 0.25 +
            self.community_score * 0.20
        )
        # 티어 자동 결정
        if self.tier_score >= 85:
            self.tier = 'S'
        elif self.tier_score >= 75:
            self.tier = 'A'
        elif self.tier_score >= 60:
            self.tier = 'B'
        elif self.tier_score >= 45:
            self.tier = 'C'
        else:
            self.tier = 'D'
        super().save(*args, **kwargs)
