from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from brands.models import Category, Brand

User = get_user_model()


class Product(models.Model):
    """
    제품(모델) 정보의 핵심 테이블.
    카테고리에 관계없이 공통 필드만 포함하고,
    카테고리별 스펙/점수는 ProductSpec/ProductScore로 관리.
    """
    TIER_CHOICES = [
        ('S', 'S티어'),
        ('A', 'A티어'),
        ('B', 'B티어'),
        ('C', 'C티어'),
        ('D', 'D티어'),
    ]

    # 기본 정보 (모든 카테고리 공통)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='브랜드'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='카테고리'
    )
    name = models.CharField(max_length=200, verbose_name='제품명')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='슬러그')
    image_url = models.URLField(blank=True, verbose_name='이미지 URL')
    description = models.TextField(blank=True, verbose_name='설명')

    # 티어 정보
    tier = models.CharField(max_length=1, choices=TIER_CHOICES, default='C', verbose_name='티어')
    tier_score = models.FloatField(default=0.0, verbose_name='티어 점수')
    community_tier = models.CharField(
        max_length=1,
        choices=TIER_CHOICES,
        null=True,
        blank=True,
        verbose_name='커뮤니티 티어'
    )

    # 카테고리별 분류 (Category.filter_definitions에서 선택지 정의)
    product_type = models.CharField(max_length=50, blank=True, verbose_name='제품 타입')
    usage = models.CharField(max_length=50, blank=True, verbose_name='용도')

    # 가격 정보
    price_min = models.IntegerField(default=0, verbose_name='최저가')
    price_max = models.IntegerField(default=0, verbose_name='최고가')

    # 제휴 링크
    coupang_link = models.URLField(blank=True, verbose_name='쿠팡 링크')
    naver_link = models.URLField(blank=True, verbose_name='네이버 링크')

    # 버전 정보
    release_year = models.IntegerField(null=True, blank=True, verbose_name='출시년도')
    version_number = models.IntegerField(default=1, verbose_name='버전')
    prev_version = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_versions',
        verbose_name='이전 버전'
    )

    # 메타
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '제품'
        verbose_name_plural = '제품'
        ordering = ['-tier_score', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['tier']),
            models.Index(fields=['product_type', 'usage']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}", allow_unicode=True)
        # 티어 점수 기반으로 티어 자동 결정
        self.tier = self.calculate_tier()
        super().save(*args, **kwargs)

    @property
    def review_count(self):
        return self.reviews.filter(is_visible=True).count()

    def calculate_tier(self):
        """티어 점수를 기반으로 티어 결정"""
        if self.tier_score >= 85:
            return 'S'
        elif self.tier_score >= 75:
            return 'A'
        elif self.tier_score >= 60:
            return 'B'
        elif self.tier_score >= 45:
            return 'C'
        return 'D'

    def get_specs_dict(self):
        """스펙을 딕셔너리로 반환"""
        return {spec.key: spec.value for spec in self.specs.all()}

    def get_scores_dict(self):
        """점수를 딕셔너리로 반환"""
        return {score.key: score.value for score in self.scores.all()}

    def calculate_tier_score(self):
        """카테고리 정의에 따라 티어 점수 계산"""
        score_defs = self.category.score_definitions or []
        if not score_defs:
            return self.tier_score

        scores = self.get_scores_dict()
        total_weight = sum(d.get('weight', 0) for d in score_defs)
        if total_weight == 0:
            return 0

        weighted_sum = 0
        for score_def in score_defs:
            key = score_def.get('key')
            weight = score_def.get('weight', 0)
            value = scores.get(key, 0)
            weighted_sum += float(value) * weight

        return weighted_sum / total_weight * 100 if total_weight else 0


class ProductSpec(models.Model):
    """
    제품별 동적 스펙 정보.
    카테고리의 spec_definitions에 정의된 키를 사용.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specs',
        verbose_name='제품'
    )
    key = models.CharField(max_length=100, verbose_name='스펙 키')
    value = models.CharField(max_length=200, verbose_name='값')

    class Meta:
        verbose_name = '제품 스펙'
        verbose_name_plural = '제품 스펙'
        unique_together = ['product', 'key']

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"


class ProductScore(models.Model):
    """
    제품별 동적 점수 정보.
    카테고리의 score_definitions에 정의된 키를 사용.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='제품'
    )
    key = models.CharField(max_length=100, verbose_name='점수 키')
    value = models.FloatField(default=0.0, verbose_name='점수')

    class Meta:
        verbose_name = '제품 점수'
        verbose_name_plural = '제품 점수'
        unique_together = ['product', 'key']

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"


class ProductTrap(models.Model):
    """
    제품별 함정 정보.
    카테고리마다 다른 함정 유형을 가질 수 있음.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='traps',
        verbose_name='제품'
    )
    trap_type = models.CharField(max_length=50, verbose_name='함정 유형')
    trap_description = models.TextField(verbose_name='함정 설명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '제품 함정'
        verbose_name_plural = '제품 함정'

    def __str__(self):
        return f"{self.product.name} - {self.trap_type}"


# 하위 호환성을 위한 별칭 (기존 코드에서 ShoeModel 사용 시)
ShoeModel = Product
ModelSpec = ProductSpec
ModelTrap = ProductTrap


class ProductComment(models.Model):
    """공식 계급도 제품 댓글 (오픈 계급도 TierChartComment와 유사)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='제품'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_comments',
        verbose_name='작성자'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='상위 댓글'
    )
    content = models.TextField(max_length=1000, verbose_name='내용')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '제품 댓글'
        verbose_name_plural = '제품 댓글'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"


class Post(models.Model):
    """통합 게시판 게시글 (자유토론, 제품후기, 질문)"""
    TAG_CHOICES = [
        ('free', '자유토론'),
        ('product_review', '제품후기'),
        ('question', '질문'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='카테고리'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='작성자'
    )
    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        default='free',
        verbose_name='태그'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='board_posts',
        verbose_name='관련 제품'
    )
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    comment_count = models.IntegerField(default=0, verbose_name='댓글 수')
    is_notice = models.BooleanField(default=False, verbose_name='공지사항')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글'
        ordering = ['-is_notice', '-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['-is_notice', '-created_at']),
            models.Index(fields=['category', 'tag', '-created_at']),
            models.Index(fields=['product', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def increase_view_count(self):
        """조회수 증가 (F expression 사용)"""
        Post.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)


class PostComment(models.Model):
    """게시글 댓글"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='게시글'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_comments',
        verbose_name='작성자'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='상위 댓글'
    )
    content = models.TextField(max_length=1000, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '게시글 댓글'
        verbose_name_plural = '게시글 댓글'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # 댓글 생성 시 게시글의 comment_count 증가
            Post.objects.filter(pk=self.post_id).update(
                comment_count=F('comment_count') + 1
            )

    def delete(self, *args, **kwargs):
        post_id = self.post_id
        super().delete(*args, **kwargs)
        # 댓글 삭제 시 게시글의 comment_count 감소
        Post.objects.filter(pk=post_id).update(
            comment_count=F('comment_count') - 1
        )


class PostLike(models.Model):
    """게시글 좋아요"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='게시글'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name='사용자'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    class Meta:
        verbose_name = '게시글 좋아요'
        verbose_name_plural = '게시글 좋아요'
        unique_together = ['post', 'user']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Post.objects.filter(pk=self.post_id).update(
                like_count=F('like_count') + 1
            )

    def delete(self, *args, **kwargs):
        post_id = self.post_id
        super().delete(*args, **kwargs)
        Post.objects.filter(pk=post_id).update(
            like_count=F('like_count') - 1
        )
