# 계급도 (Gyegeupdo) 전체 시스템 검토 리포트

**작성일**: 2026-03-07
**검토 범위**: Backend (Django) + Frontend (Next.js) 전체

## 요약

현재 사이트는 **MVP 수준에서 잘 작동**하지만, 카테고리와 데이터가 늘어날 때 **반드시 잡아야 할 구조적 문제**들이 있습니다. 아래 우선순위별로 정리했습니다.

---

## 🔴 즉시 수정 (데이터 늘기 전에 반드시)

### 1. 프론트엔드 카테고리 하드코딩 — 13개 파일에 분산

새 카테고리를 추가하려면 **최소 13개 파일**을 수동으로 수정해야 합니다. API 기반 구조를 만들었지만 프론트엔드가 아직 활용하지 않고 있습니다.

| 파일 | 하드코딩 내용 |
|------|-------------|
| `Sidebar.tsx:17` | CATEGORIES 배열 (slug, name, icon) |
| `Header.tsx:17` | CATEGORIES 배열 (중복) |
| `AllCategoriesOverview.tsx:39` | CATEGORIES + TICKER + HOT_DISPUTES + REVIEWS |
| `CategoryLandingContent.tsx:40` | CATEGORY_CONFIG + USAGE_CATEGORIES + USAGE_TIER_DATA |
| `BoardContent.tsx:45` | CATEGORY_CONFIG + MOCK_POSTS |
| `BoardPostDetailContent.tsx:27` | CATEGORY_CONFIG import |
| `QuizContent.tsx:69` | CATEGORY_CONFIG |
| `DiscoverContent.tsx:13` | CATEGORY_INFO |
| `CompareContent.tsx:29` | CATEGORY_INFO |
| `sitemap.ts:17` | URL 목록 하드코딩 |
| `[category]/page.tsx` | CATEGORY_META |
| `sidebarStore.ts:22` | 기본값 'running-shoes' |
| `tier/page.tsx`, `quiz/page.tsx` | 리다이렉트 'running-shoes' 고정 |

**영향**: 4번째 카테고리 추가 시 실수로 빠뜨리는 파일이 생기면 빌드는 되지만 런타임에 깨집니다.

### 2. 백엔드 `select_related` 버그 — 3개 뷰 깨져 있음

모델명이 `model` → `product`로 변경되었는데, 3개 뷰가 **옛 필드명**을 참조 중입니다:

```
tiers/views.py:23   → select_related('model', 'user')         # 'product' 이어야 함
tiers/views.py:94   → select_related('model', 'model__brand')  # 'product', 'product__brand'
reviews/views.py:10 → select_related('user', 'model')          # 'user', 'product'
```

**영향**: 해당 API 호출 시 에러 발생 가능. 현재는 데이터가 없어서 발견되지 않은 것.

### 3. 보안 기본값 — 프로덕션 위험

```python
# config/settings.py:18
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
# config/settings.py:21
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

Railway에서 환경변수가 설정되어 있으면 괜찮지만, **실수로 빠지면 프로덕션이 DEBUG=True**로 돌아갑니다. 기본값을 `False`로 바꿔야 합니다.

---

## 🟠 높은 우선순위 (데이터 100건 넘기 전에)

### 4. API Rate Limiting 없음

현재 **모든 API에 속도 제한이 없습니다**. 누구든 초당 수천 건 요청 가능.

**영향**: 크롤러/봇이 DB 과부하 유발 가능. DRF의 `AnonRateThrottle`, `UserRateThrottle` 추가 필요.

### 5. 캐싱 전무 — Redis 있지만 미사용

Redis가 설정되어 있지만, **단 한 곳에서도 사용되지 않습니다**:
- `@cache_page()` 데코레이터: 0건
- `cache.get()`/`cache.set()`: 0건

카테고리 정의, 브랜드 목록 같은 **거의 변하지 않는 데이터**가 매 요청마다 DB 쿼리됩니다.

**권장**: 카테고리/브랜드 목록에 5분 캐시만 걸어도 DB 부하 80% 감소.

### 6. 프론트엔드 Mock 데이터 번들 비대 — 205KB

| 파일 | 크기 |
|------|------|
| `mockProducts.ts` | 144 KB |
| `mockData.ts` | 61 KB |
| **합계** | **205 KB** |

이 데이터가 **API 성공 여부와 관계없이** 항상 클라이언트에 다운로드됩니다. 트리쉐이킹이 불가능합니다 (직접 import).

**권장**: API가 안정화되면 mock 데이터를 `dynamic import`로 전환하거나 제거.

### 7. Procfile에 seed_categories — 매 배포마다 실행

```
web: python manage.py migrate && python manage.py seed_categories && ...
```

`update_or_create`라 데이터가 꼬이진 않지만, 매 배포마다 **~260건의 DB 쿼리**를 실행합니다. 카테고리가 10개, 브랜드가 200개가 되면 배포 시간이 길어집니다.

**권장**: 한 번 시딩 후 Procfile에서 제거. 이후 Django Admin으로 관리.

---

## 🟡 중간 우선순위 (서비스 성장 대비)

### 8. N+1 쿼리 패턴

시리얼라이저에서 `SerializerMethodField`로 카운트를 구하는 부분:

```python
# brands/serializers.py - CategoryListSerializer
def get_product_count(self, obj):
    return obj.products.filter(is_active=True).count()  # 카테고리마다 1쿼리
def get_brand_count(self, obj):
    return obj.brands.filter(is_active=True).count()    # 카테고리마다 1쿼리
```

카테고리 10개면 목록 조회 시 **20개 추가 쿼리** 발생. `annotate(Count(...))`로 1쿼리로 해결 가능.

### 9. DB 인덱스 부족

현재 인덱스가 없는 자주 조회되는 필드들:

| 모델 | 필요한 인덱스 |
|------|-------------|
| Category | `(is_active, display_order)` |
| Product | `(category, is_active)`, `(brand, is_active)` |
| Review | `(product, is_visible)` |
| QuizSession | `session_key`, `user`, `category` |
| TierChartComment | `(tier_chart, created_at)` |

### 10. 페이지네이션 누락 엔드포인트

| 엔드포인트 | 상태 |
|----------|------|
| `GET /categories/` | 페이지네이션 없음 |
| `GET /reviews/` | 페이지네이션 없음 |
| `GET /brands/{slug}/products/` | 페이지네이션 없음 |

### 11. 경쟁 상태 (Race Condition)

좋아요/댓글 수 같은 비정규화된 카운트가 `save()` 내에서 직접 증감됩니다:

```python
# tiers/models.py - TierChartLike.save()
self.tier_chart.like_count += 1
self.tier_chart.save()  # 동시 요청 시 카운트 유실
```

**권장**: `F('like_count') + 1` 또는 `select_for_update()` 사용.

### 12. 하드코딩된 비즈니스 로직

| 위치 | 하드코딩 값 |
|------|-----------|
| `Brand._calculate_tier_score()` | S>=85, A>=75, B>=60, C>=45 |
| `TierDispute.update_status()` | 지지 30표 이상 시 콜로세움 진입 |
| `UserProfile.update_badge()` | 리뷰 5/20/50/100건 기준 |
| `seo_pages/views.py` | '2026년' 하드코딩 |
| `models_app/serializers.py` | '2026' 하드코딩 |

---

## 🟢 장기 개선 (서비스 안정화 후)

| 항목 | 설명 |
|------|------|
| API 문서화 | drf-spectacular으로 OpenAPI 스펙 자동 생성 |
| 풀텍스트 검색 | PostgreSQL trigram 또는 Elasticsearch |
| 비동기 작업 | Celery + Redis (티어 재계산, 이메일 등) |
| CDN | CloudFront로 이미지/정적 파일 배포 |
| 테스트 | 현재 테스트 코드 0건. 최소 API 엔드포인트 테스트 필요 |
| 모니터링 | Sentry 에러 추적, 슬로우 쿼리 로깅 |
| Soft Delete | 삭제 데이터 복구 불가 → `is_deleted` 필드 추가 |

---

## 액션 플랜 (추천 순서)

| 순서 | 작업 | 예상 난이도 | 영향도 |
|------|------|-----------|--------|
| 1 | `select_related` 버그 수정 (3파일) | 낮음 | 크리티컬 |
| 2 | DEBUG 기본값 False로 변경 | 낮음 | 크리티컬 |
| 3 | Procfile에서 seed_categories 제거 | 낮음 | 중간 |
| 4 | Rate Limiting 추가 | 낮음 | 높음 |
| 5 | 프론트엔드 Header/Sidebar API 연동 | 중간 | 높음 |
| 6 | 카테고리 목록 캐싱 | 낮음 | 높음 |
| 7 | N+1 쿼리 수정 (annotate) | 중간 | 중간 |
| 8 | Race condition 수정 (F expression) | 중간 | 중간 |
