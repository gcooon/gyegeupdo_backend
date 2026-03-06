from rest_framework.decorators import api_view
from rest_framework.response import Response
from models_app.models import Product
from brands.models import Category


@api_view(['GET'])
def seo_landing(request):
    """SEO 랜딩 페이지 데이터 생성"""
    keyword = request.query_params.get('keyword', '')
    category_slug = request.query_params.get('category', 'running-shoes')

    # 카테고리 조회
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None

    # 키워드 분석하여 필터 프리셋 생성
    preset = {}
    related_keywords = []

    if '평발' in keyword or '과내전' in keyword:
        preset['pronation'] = 'overpronation'
        related_keywords = ['평발 과내전 러닝화', '안정성 러닝화 계급도']
    elif '요족' in keyword or '과외전' in keyword:
        preset['pronation'] = 'supination'
        related_keywords = ['요족 러닝화 추천', '쿠션 러닝화 계급도']

    if '넓은' in keyword or '발볼' in keyword:
        preset['foot_width'] = 'wide'
        related_keywords.append('넓은 발볼 러닝화 계급도')

    if '입문' in keyword or '초보' in keyword:
        preset['usage'] = 'beginner'
        related_keywords.append('초보 러닝화 추천')
    elif '레이싱' in keyword or '대회' in keyword:
        preset['usage'] = 'race'
        related_keywords.append('마라톤 러닝화 계급도')

    # 제품 조회
    queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')

    if category:
        queryset = queryset.filter(category=category)
    if preset.get('usage'):
        queryset = queryset.filter(usage=preset['usage'])

    top_products = queryset.order_by('-tier_score')[:10]

    products_data = [{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'brand_name': p.brand.name,
        'tier': p.tier,
        'tier_score': p.tier_score,
        'image_url': p.image_url
    } for p in top_products]

    category_name = category.name if category else '제품'

    return Response({
        'success': True,
        'data': {
            'title': f"2026년 {keyword} 계급도" if keyword else f"2026년 {category_name} 계급도",
            'preset': preset,
            'top_products': products_data,
            'related_keywords': related_keywords
        },
        'message': 'OK'
    })
