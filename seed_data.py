"""Seed data script for multi-category architecture"""
import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from brands.models import Category, Brand
from models_app.models import Product, ProductSpec, ProductScore

# 카테고리 생성 (런닝화)
running_shoes_category, _ = Category.objects.update_or_create(
    slug='running-shoes',
    defaults={
        'name': '런닝화',
        'icon': '👟',
        'description': '러닝 및 조깅용 신발',
        'spec_definitions': [
            {'key': 'weight', 'label': '무게', 'unit': 'g', 'type': 'number'},
            {'key': 'drop', 'label': '드롭', 'unit': 'mm', 'type': 'number'},
            {'key': 'stack_height', 'label': '스택 높이', 'unit': 'mm', 'type': 'number'},
            {'key': 'width', 'label': '발볼', 'type': 'select', 'options': [
                {'value': 'narrow', 'label': '좁음'},
                {'value': 'standard', 'label': '표준'},
                {'value': 'wide', 'label': '넓음'},
                {'value': 'extra_wide', 'label': '매우 넓음'}
            ]},
            {'key': 'upper_material', 'label': '갑피 소재', 'type': 'text'},
            {'key': 'midsole_material', 'label': '미드솔 소재', 'type': 'text'},
        ],
        'score_definitions': [
            {'key': 'cushion', 'label': '쿠션', 'weight': 25},
            {'key': 'responsiveness', 'label': '반응성', 'weight': 20},
            {'key': 'stability', 'label': '안정성', 'weight': 20},
            {'key': 'breathability', 'label': '통기성', 'weight': 15},
            {'key': 'durability', 'label': '내구성', 'weight': 20},
        ],
        'brand_score_definitions': [
            {'key': 'lineup', 'label': '라인업', 'weight': 25},
            {'key': 'tech', 'label': '기술력', 'weight': 30},
            {'key': 'durability', 'label': '내구성', 'weight': 25},
            {'key': 'community', 'label': '커뮤니티 평가', 'weight': 20},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'daily', 'label': '데일리'},
                {'value': 'tempo', 'label': '템포'},
                {'value': 'race', 'label': '레이스'},
                {'value': 'trail', 'label': '트레일'},
            ],
            'usage': [
                {'value': 'beginner', 'label': '입문자용'},
                {'value': 'intermediate', 'label': '중급자용'},
                {'value': 'advanced', 'label': '상급자용'},
            ]
        },
        'quiz_definitions': [
            {
                'key': 'foot_width',
                'question': '발볼이 어떻게 되시나요?',
                'options': [
                    {'value': 'narrow', 'label': '좁음'},
                    {'value': 'normal', 'label': '보통'},
                    {'value': 'wide', 'label': '넓음'},
                ]
            },
            {
                'key': 'pronation',
                'question': '걸음걸이 유형이 어떻게 되시나요?',
                'options': [
                    {'value': 'overpronation', 'label': '과내전 (평발)'},
                    {'value': 'neutral', 'label': '중립'},
                    {'value': 'supination', 'label': '과외전 (요족)'},
                ]
            },
            {
                'key': 'usage',
                'question': '주로 어떤 용도로 사용하시나요?',
                'options': [
                    {'value': 'beginner', 'label': '입문/조깅'},
                    {'value': 'daily', 'label': '데일리 러닝'},
                    {'value': 'tempo', 'label': '템포/인터벌'},
                    {'value': 'race', 'label': '레이스/대회'},
                ]
            },
        ],
        'display_order': 1,
        'is_active': True
    }
)
print(f"Created category: {running_shoes_category.name}")

# 브랜드 생성
brands_data = [
    {'name': 'Nike', 'slug': 'nike', 'tier': 'S', 'tier_score': 92.0},
    {'name': 'Adidas', 'slug': 'adidas', 'tier': 'S', 'tier_score': 90.0},
    {'name': 'ASICS', 'slug': 'asics', 'tier': 'A', 'tier_score': 88.0},
    {'name': 'New Balance', 'slug': 'new-balance', 'tier': 'A', 'tier_score': 85.0},
    {'name': 'Hoka', 'slug': 'hoka', 'tier': 'A', 'tier_score': 87.0},
    {'name': 'Saucony', 'slug': 'saucony', 'tier': 'B', 'tier_score': 78.0},
]

brands = {}
for brand_data in brands_data:
    brand, _ = Brand.objects.update_or_create(
        slug=brand_data['slug'],
        defaults={
            'name': brand_data['name'],
            'category': running_shoes_category,
            'tier': brand_data['tier'],
            'tier_score': brand_data['tier_score'],
            'lineup_score': 80.0,
            'tech_score': 85.0,
            'durability_score': 80.0,
            'community_score': 82.0,
        }
    )
    brands[brand_data['slug']] = brand
    print(f"Created brand: {brand.name}")

# 제품 생성
products_data = [
    {
        'name': 'Alphafly 3',
        'slug': 'nike-alphafly-3',
        'brand': 'nike',
        'tier_score': 95.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 350000,
        'price_max': 400000,
        'specs': {'weight': '215', 'drop': '4', 'stack_height': '40', 'width': 'standard'},
        'scores': {'cushion': 90, 'responsiveness': 98, 'stability': 75, 'breathability': 85, 'durability': 70}
    },
    {
        'name': 'Vaporfly 3',
        'slug': 'nike-vaporfly-3',
        'brand': 'nike',
        'tier_score': 93.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 280000,
        'price_max': 320000,
        'specs': {'weight': '196', 'drop': '8', 'stack_height': '40', 'width': 'standard'},
        'scores': {'cushion': 85, 'responsiveness': 96, 'stability': 72, 'breathability': 88, 'durability': 65}
    },
    {
        'name': 'Pegasus 41',
        'slug': 'nike-pegasus-41',
        'brand': 'nike',
        'tier_score': 82.0,
        'product_type': 'daily',
        'usage': 'beginner',
        'price_min': 149000,
        'price_max': 169000,
        'specs': {'weight': '274', 'drop': '10', 'stack_height': '33', 'width': 'wide'},
        'scores': {'cushion': 85, 'responsiveness': 75, 'stability': 80, 'breathability': 82, 'durability': 85}
    },
    {
        'name': 'Adizero Adios Pro 3',
        'slug': 'adidas-adios-pro-3',
        'brand': 'adidas',
        'tier_score': 92.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 260000,
        'price_max': 300000,
        'specs': {'weight': '215', 'drop': '6.5', 'stack_height': '39.5', 'width': 'standard'},
        'scores': {'cushion': 88, 'responsiveness': 95, 'stability': 78, 'breathability': 85, 'durability': 72}
    },
    {
        'name': 'Ultraboost Light',
        'slug': 'adidas-ultraboost-light',
        'brand': 'adidas',
        'tier_score': 80.0,
        'product_type': 'daily',
        'usage': 'beginner',
        'price_min': 190000,
        'price_max': 230000,
        'specs': {'weight': '295', 'drop': '10', 'stack_height': '22', 'width': 'wide'},
        'scores': {'cushion': 90, 'responsiveness': 70, 'stability': 75, 'breathability': 78, 'durability': 82}
    },
    {
        'name': 'Metaspeed Sky+',
        'slug': 'asics-metaspeed-sky-plus',
        'brand': 'asics',
        'tier_score': 91.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 250000,
        'price_max': 290000,
        'specs': {'weight': '195', 'drop': '5', 'stack_height': '41', 'width': 'standard'},
        'scores': {'cushion': 86, 'responsiveness': 94, 'stability': 80, 'breathability': 84, 'durability': 68}
    },
    {
        'name': 'Gel-Nimbus 26',
        'slug': 'asics-gel-nimbus-26',
        'brand': 'asics',
        'tier_score': 83.0,
        'product_type': 'daily',
        'usage': 'beginner',
        'price_min': 180000,
        'price_max': 220000,
        'specs': {'weight': '290', 'drop': '8', 'stack_height': '34', 'width': 'wide'},
        'scores': {'cushion': 92, 'responsiveness': 72, 'stability': 85, 'breathability': 80, 'durability': 88}
    },
    {
        'name': 'SC Elite v4',
        'slug': 'new-balance-sc-elite-v4',
        'brand': 'new-balance',
        'tier_score': 89.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 240000,
        'price_max': 280000,
        'specs': {'weight': '206', 'drop': '9', 'stack_height': '38', 'width': 'standard'},
        'scores': {'cushion': 85, 'responsiveness': 92, 'stability': 77, 'breathability': 82, 'durability': 70}
    },
    {
        'name': 'Fresh Foam 1080 v13',
        'slug': 'new-balance-1080-v13',
        'brand': 'new-balance',
        'tier_score': 81.0,
        'product_type': 'daily',
        'usage': 'beginner',
        'price_min': 170000,
        'price_max': 210000,
        'specs': {'weight': '295', 'drop': '6', 'stack_height': '31', 'width': 'extra_wide'},
        'scores': {'cushion': 90, 'responsiveness': 74, 'stability': 82, 'breathability': 78, 'durability': 85}
    },
    {
        'name': 'Rocket X 2',
        'slug': 'hoka-rocket-x2',
        'brand': 'hoka',
        'tier_score': 90.0,
        'product_type': 'race',
        'usage': 'advanced',
        'price_min': 230000,
        'price_max': 270000,
        'specs': {'weight': '213', 'drop': '5', 'stack_height': '40', 'width': 'standard'},
        'scores': {'cushion': 88, 'responsiveness': 93, 'stability': 76, 'breathability': 83, 'durability': 68}
    },
    {
        'name': 'Clifton 9',
        'slug': 'hoka-clifton-9',
        'brand': 'hoka',
        'tier_score': 84.0,
        'product_type': 'daily',
        'usage': 'beginner',
        'price_min': 160000,
        'price_max': 190000,
        'specs': {'weight': '248', 'drop': '5', 'stack_height': '32', 'width': 'wide'},
        'scores': {'cushion': 92, 'responsiveness': 75, 'stability': 80, 'breathability': 82, 'durability': 80}
    },
]

for product_data in products_data:
    product, _ = Product.objects.update_or_create(
        slug=product_data['slug'],
        defaults={
            'name': product_data['name'],
            'brand': brands[product_data['brand']],
            'category': running_shoes_category,
            'tier_score': product_data['tier_score'],
            'product_type': product_data['product_type'],
            'usage': product_data['usage'],
            'price_min': product_data['price_min'],
            'price_max': product_data['price_max'],
        }
    )

    # 스펙 추가
    for key, value in product_data['specs'].items():
        ProductSpec.objects.update_or_create(
            product=product,
            key=key,
            defaults={'value': str(value)}
        )

    # 점수 추가
    for key, value in product_data['scores'].items():
        ProductScore.objects.update_or_create(
            product=product,
            key=key,
            defaults={'value': float(value)}
        )

    print(f"Created product: {product.brand.name} {product.name} (Tier {product.tier})")

print("\nSeed data created successfully!")
