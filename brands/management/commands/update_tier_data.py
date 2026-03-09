"""
계급도 데이터 대규모 업데이트 커맨드
- 치킨: 메뉴 종류별 계급도 (후라이드/양념/간장/마늘/치즈/순살)
- 러닝화: 브랜드 S~D 확장 + 제품 데이터 보강
- 시계: 데이터 보강

커뮤니티 데이터 기반으로 실제 인정받는 계급도 반영
"""
from django.core.management.base import BaseCommand
from brands.models import Category, Brand, BrandScore
from models_app.models import Product, ProductScore


class Command(BaseCommand):
    help = '계급도 데이터 대규모 업데이트'

    def handle(self, *args, **options):
        self.update_chicken()
        self.update_running_shoes()
        self.update_watches()
        self.stdout.write(self.style.SUCCESS('전체 데이터 업데이트 완료!'))

    def update_chicken(self):
        """치킨 카테고리 - 메뉴 종류별 계급도"""
        self.stdout.write('=' * 50)
        self.stdout.write('치킨 카테고리 업데이트 중...')

        category = Category.objects.get(slug='chicken')

        # 1. filter_definitions - 메뉴 종류 중심으로 변경
        category.filter_definitions = {
            'product_type': [
                {'value': 'fried', 'label': '후라이드', 'description': '바삭한 기본 후라이드 치킨', 'icon': '🍗'},
                {'value': 'seasoned', 'label': '양념', 'description': '달콤 매콤한 양념 치킨', 'icon': '🌶️'},
                {'value': 'soy', 'label': '간장/허니', 'description': '달콤짭짤한 간장 소스', 'icon': '🍯'},
                {'value': 'garlic', 'label': '마늘/파닭', 'description': '마늘&파 풍미 치킨', 'icon': '🧄'},
                {'value': 'cheese', 'label': '치즈', 'description': '치즈 시즈닝/토핑 치킨', 'icon': '🧀'},
                {'value': 'boneless', 'label': '순살', 'description': '뼈 없는 순살 치킨', 'icon': '🥢'},
                {'value': 'roasted', 'label': '구이/훈제', 'description': '오븐구이, 훈제 치킨', 'icon': '🔥'},
                {'value': 'spicy', 'label': '매운맛', 'description': '청양/불닭 등 매운 치킨', 'icon': '🔥'},
            ],
        }
        category.save()
        self.stdout.write('  filter_definitions 업데이트 완료')

        # 2. 브랜드 전체 정비 (S~D 티어)
        brands_data = [
            # S티어 - 프리미엄 대형 프랜차이즈
            {'name': 'BBQ', 'slug': 'bbq', 'tier': 'S', 'tier_score': 92,
             'description': '황금올리브로 유명, 프리미엄 치킨의 대명사',
             'scores': {'taste': 95, 'price': 70, 'crispy': 95, 'popularity': 95}},
            {'name': '교촌치킨', 'slug': 'kyochon', 'tier': 'S', 'tier_score': 90,
             'description': '허니콤보의 원조, 간장치킨 1등',
             'scores': {'taste': 92, 'price': 72, 'crispy': 88, 'popularity': 95}},
            {'name': 'BHC', 'slug': 'bhc', 'tier': 'S', 'tier_score': 88,
             'description': '뿌링클의 신화, 치즈치킨 강자',
             'scores': {'taste': 90, 'price': 75, 'crispy': 90, 'popularity': 92}},

            # A티어 - 인기 대형 프랜차이즈
            {'name': '굽네치킨', 'slug': 'goobne', 'tier': 'A', 'tier_score': 82,
             'description': '오븐구이 치킨의 선두주자',
             'scores': {'taste': 85, 'price': 75, 'crispy': 75, 'popularity': 85}},
            {'name': '네네치킨', 'slug': 'nene', 'tier': 'A', 'tier_score': 80,
             'description': '스노윙, 파닭 등 다양한 메뉴',
             'scores': {'taste': 82, 'price': 78, 'crispy': 80, 'popularity': 82}},
            {'name': '푸라닭', 'slug': 'puradak', 'tier': 'A', 'tier_score': 78,
             'description': '블랙알리오 등 프리미엄 메뉴',
             'scores': {'taste': 82, 'price': 70, 'crispy': 78, 'popularity': 78}},
            {'name': '지코바', 'slug': 'jicoba', 'tier': 'A', 'tier_score': 76,
             'description': '매콤한 닭볶음탕 스타일',
             'scores': {'taste': 80, 'price': 78, 'crispy': 70, 'popularity': 75}},

            # B티어 - 중견 프랜차이즈
            {'name': '처갓집양념치킨', 'slug': 'cheogajip', 'tier': 'B', 'tier_score': 72,
             'description': '양념치킨 전문, 가성비 좋음',
             'scores': {'taste': 75, 'price': 82, 'crispy': 70, 'popularity': 72}},
            {'name': '호식이두마리치킨', 'slug': 'hosigi', 'tier': 'B', 'tier_score': 74,
             'description': '2마리 치킨의 원조, 가성비 최강',
             'scores': {'taste': 70, 'price': 95, 'crispy': 72, 'popularity': 78}},
            {'name': '페리카나', 'slug': 'pelicana', 'tier': 'B', 'tier_score': 70,
             'description': '오랜 전통의 양념치킨',
             'scores': {'taste': 72, 'price': 80, 'crispy': 68, 'popularity': 68}},
            {'name': '자담치킨', 'slug': 'jadam', 'tier': 'B', 'tier_score': 68,
             'description': '매콤한 맛이 특징',
             'scores': {'taste': 72, 'price': 78, 'crispy': 65, 'popularity': 62}},
            {'name': '멕시카나', 'slug': 'mexicana', 'tier': 'B', 'tier_score': 66,
             'description': '국내 최초 프랜차이즈 치킨',
             'scores': {'taste': 68, 'price': 80, 'crispy': 65, 'popularity': 60}},
            {'name': '또래오래', 'slug': 'ttorae', 'tier': 'B', 'tier_score': 65,
             'description': '가성비 좋은 동네 치킨',
             'scores': {'taste': 65, 'price': 88, 'crispy': 62, 'popularity': 58}},

            # C티어 - 가성비/저가 프랜차이즈
            {'name': '60계치킨', 'slug': '60gye', 'tier': 'C', 'tier_score': 55,
             'description': '6000원대 초저가 치킨',
             'scores': {'taste': 52, 'price': 98, 'crispy': 50, 'popularity': 55}},
            {'name': '노랑통닭', 'slug': 'norang', 'tier': 'C', 'tier_score': 52,
             'description': '옛날 통닭 스타일',
             'scores': {'taste': 55, 'price': 88, 'crispy': 48, 'popularity': 50}},
            {'name': '땅땅치킨', 'slug': 'ddangddang', 'tier': 'C', 'tier_score': 50,
             'description': '저가형 프랜차이즈',
             'scores': {'taste': 48, 'price': 92, 'crispy': 45, 'popularity': 45}},
            {'name': '스모프치킨', 'slug': 'smof', 'tier': 'C', 'tier_score': 48,
             'description': '훈제치킨 전문',
             'scores': {'taste': 52, 'price': 78, 'crispy': 42, 'popularity': 42}},
            {'name': '오븐마루', 'slug': 'ovenmaru', 'tier': 'C', 'tier_score': 55,
             'description': '오븐구이 치킨',
             'scores': {'taste': 58, 'price': 75, 'crispy': 50, 'popularity': 52}},

            # D티어 - 비추천
            {'name': '편의점치킨', 'slug': 'convenience', 'tier': 'D', 'tier_score': 35,
             'description': 'GS25, CU 등 편의점 치킨',
             'scores': {'taste': 35, 'price': 70, 'crispy': 25, 'popularity': 40}},
            {'name': '마트델리치킨', 'slug': 'mart-deli', 'tier': 'D', 'tier_score': 38,
             'description': '이마트, 홈플러스 등 델리코너',
             'scores': {'taste': 40, 'price': 80, 'crispy': 30, 'popularity': 42}},
            {'name': '냉동치킨', 'slug': 'frozen', 'tier': 'D', 'tier_score': 30,
             'description': '마트 냉동식품 치킨',
             'scores': {'taste': 30, 'price': 85, 'crispy': 20, 'popularity': 25}},
        ]

        for brand_data in brands_data:
            # 1. 브랜드 기본 정보만 먼저 생성/업데이트
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'description': brand_data.get('description', ''),
                    'is_active': True,
                }
            )

            # 2. BrandScore 추가
            if 'scores' in brand_data:
                for key, value in brand_data['scores'].items():
                    BrandScore.objects.update_or_create(
                        brand=brand,
                        key=key,
                        defaults={'value': value, 'label': key}
                    )

            # 3. tier와 tier_score를 직접 DB 업데이트 (save() 우회 - 마지막에 강제 설정)
            Brand.objects.filter(pk=brand.pk).update(
                tier=brand_data['tier'],
                tier_score=brand_data['tier_score']
            )

            action = '추가' if created else '업데이트'
            self.stdout.write(f'  브랜드 {action}: {brand.name} ({brand_data["tier"]}티어)')

        # 3. 제품 데이터 - 메뉴 종류별로 풍성하게
        products_data = [
            # === 후라이드 ===
            {'brand': 'bbq', 'name': '황금올리브 후라이드', 'product_type': 'fried', 'tier': 'S', 'tier_score': 95},
            {'brand': 'bbq', 'name': '자메이카 통다리', 'product_type': 'fried', 'tier': 'A', 'tier_score': 82},
            {'brand': 'kyochon', 'name': '교촌 오리지널', 'product_type': 'fried', 'tier': 'S', 'tier_score': 90},
            {'brand': 'bhc', 'name': '맛초킹', 'product_type': 'fried', 'tier': 'A', 'tier_score': 85},
            {'brand': 'bhc', 'name': 'BHC 후라이드', 'product_type': 'fried', 'tier': 'A', 'tier_score': 82},
            {'brand': 'goobne', 'name': '굽네 오리지널', 'product_type': 'fried', 'tier': 'A', 'tier_score': 80},
            {'brand': 'nene', 'name': '네네 후라이드', 'product_type': 'fried', 'tier': 'A', 'tier_score': 78},
            {'brand': 'puradak', 'name': '푸라닭 후라이드', 'product_type': 'fried', 'tier': 'A', 'tier_score': 76},
            {'brand': 'cheogajip', 'name': '처갓집 후라이드', 'product_type': 'fried', 'tier': 'B', 'tier_score': 70},
            {'brand': 'hosigi', 'name': '호식이 후라이드', 'product_type': 'fried', 'tier': 'B', 'tier_score': 72},
            {'brand': 'pelicana', 'name': '페리카나 후라이드', 'product_type': 'fried', 'tier': 'B', 'tier_score': 68},
            {'brand': 'mexicana', 'name': '멕시카나 후라이드', 'product_type': 'fried', 'tier': 'B', 'tier_score': 65},
            {'brand': 'ttorae', 'name': '또래오래 후라이드', 'product_type': 'fried', 'tier': 'B', 'tier_score': 62},
            {'brand': '60gye', 'name': '60계 후라이드', 'product_type': 'fried', 'tier': 'C', 'tier_score': 52},
            {'brand': 'norang', 'name': '노랑통닭 후라이드', 'product_type': 'fried', 'tier': 'C', 'tier_score': 50},
            {'brand': 'ddangddang', 'name': '땅땅 후라이드', 'product_type': 'fried', 'tier': 'C', 'tier_score': 48},

            # === 양념 ===
            {'brand': 'kyochon', 'name': '교촌 레드콤보', 'product_type': 'seasoned', 'tier': 'S', 'tier_score': 92},
            {'brand': 'bbq', 'name': 'BBQ 양념치킨', 'product_type': 'seasoned', 'tier': 'S', 'tier_score': 88},
            {'brand': 'bhc', 'name': 'BHC 양념치킨', 'product_type': 'seasoned', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nene', 'name': '네네 양념치킨', 'product_type': 'seasoned', 'tier': 'A', 'tier_score': 80},
            {'brand': 'goobne', 'name': '굽네 고추바사삭', 'product_type': 'seasoned', 'tier': 'A', 'tier_score': 78},
            {'brand': 'cheogajip', 'name': '처갓집 양념치킨', 'product_type': 'seasoned', 'tier': 'B', 'tier_score': 75},
            {'brand': 'pelicana', 'name': '페리카나 양념치킨', 'product_type': 'seasoned', 'tier': 'B', 'tier_score': 70},
            {'brand': 'hosigi', 'name': '호식이 양념치킨', 'product_type': 'seasoned', 'tier': 'B', 'tier_score': 68},
            {'brand': 'mexicana', 'name': '멕시카나 양념치킨', 'product_type': 'seasoned', 'tier': 'B', 'tier_score': 65},
            {'brand': '60gye', 'name': '60계 양념치킨', 'product_type': 'seasoned', 'tier': 'C', 'tier_score': 52},
            {'brand': 'norang', 'name': '노랑통닭 양념', 'product_type': 'seasoned', 'tier': 'C', 'tier_score': 50},

            # === 간장/허니 ===
            {'brand': 'kyochon', 'name': '교촌 허니콤보', 'product_type': 'soy', 'tier': 'S', 'tier_score': 95},
            {'brand': 'kyochon', 'name': '교촌 허니오리지널', 'product_type': 'soy', 'tier': 'S', 'tier_score': 92},
            {'brand': 'bbq', 'name': 'BBQ 허니갈릭', 'product_type': 'soy', 'tier': 'A', 'tier_score': 85},
            {'brand': 'nene', 'name': '네네 스노윙', 'product_type': 'soy', 'tier': 'A', 'tier_score': 82},
            {'brand': 'bhc', 'name': 'BHC 소이갈릭', 'product_type': 'soy', 'tier': 'A', 'tier_score': 80},
            {'brand': 'puradak', 'name': '푸라닭 간장치킨', 'product_type': 'soy', 'tier': 'A', 'tier_score': 78},
            {'brand': 'jadam', 'name': '자담치킨 간장치킨', 'product_type': 'soy', 'tier': 'B', 'tier_score': 68},
            {'brand': 'pelicana', 'name': '페리카나 간장치킨', 'product_type': 'soy', 'tier': 'B', 'tier_score': 65},
            {'brand': '60gye', 'name': '60계 간장치킨', 'product_type': 'soy', 'tier': 'C', 'tier_score': 50},

            # === 마늘/파닭 ===
            {'brand': 'bbq', 'name': 'BBQ 마늘치킨', 'product_type': 'garlic', 'tier': 'S', 'tier_score': 88},
            {'brand': 'nene', 'name': '네네 파닭', 'product_type': 'garlic', 'tier': 'S', 'tier_score': 90},
            {'brand': 'puradak', 'name': '푸라닭 블랙알리오', 'product_type': 'garlic', 'tier': 'A', 'tier_score': 85},
            {'brand': 'bhc', 'name': 'BHC 마늘킹', 'product_type': 'garlic', 'tier': 'A', 'tier_score': 82},
            {'brand': 'goobne', 'name': '굽네 갈릭치킨', 'product_type': 'garlic', 'tier': 'A', 'tier_score': 78},
            {'brand': 'pelicana', 'name': '페리카나 마늘치킨', 'product_type': 'garlic', 'tier': 'B', 'tier_score': 68},
            {'brand': 'cheogajip', 'name': '처갓집 마늘치킨', 'product_type': 'garlic', 'tier': 'B', 'tier_score': 65},

            # === 치즈 ===
            {'brand': 'bhc', 'name': '뿌링클', 'product_type': 'cheese', 'tier': 'S', 'tier_score': 95},
            {'brand': 'bhc', 'name': '뿌링클 맵싹', 'product_type': 'cheese', 'tier': 'S', 'tier_score': 88},
            {'brand': 'goobne', 'name': '굽네 볼케이노', 'product_type': 'cheese', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nene', 'name': '네네 스노윙 치즈', 'product_type': 'cheese', 'tier': 'A', 'tier_score': 80},
            {'brand': 'bbq', 'name': 'BBQ 치즈볼', 'product_type': 'cheese', 'tier': 'A', 'tier_score': 78},
            {'brand': 'puradak', 'name': '푸라닭 치즈치킨', 'product_type': 'cheese', 'tier': 'B', 'tier_score': 72},
            {'brand': 'cheogajip', 'name': '처갓집 치즈치킨', 'product_type': 'cheese', 'tier': 'B', 'tier_score': 68},

            # === 순살 ===
            {'brand': 'bbq', 'name': '황금올리브 순살', 'product_type': 'boneless', 'tier': 'S', 'tier_score': 92},
            {'brand': 'kyochon', 'name': '교촌 순살', 'product_type': 'boneless', 'tier': 'S', 'tier_score': 88},
            {'brand': 'bhc', 'name': 'BHC 순살치킨', 'product_type': 'boneless', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nene', 'name': '네네 순살치킨', 'product_type': 'boneless', 'tier': 'A', 'tier_score': 80},
            {'brand': 'goobne', 'name': '굽네 순살치킨', 'product_type': 'boneless', 'tier': 'A', 'tier_score': 78},
            {'brand': 'puradak', 'name': '푸라닭 순살', 'product_type': 'boneless', 'tier': 'B', 'tier_score': 72},
            {'brand': 'cheogajip', 'name': '처갓집 순살', 'product_type': 'boneless', 'tier': 'B', 'tier_score': 68},
            {'brand': 'hosigi', 'name': '호식이 순살', 'product_type': 'boneless', 'tier': 'B', 'tier_score': 65},

            # === 구이/훈제 ===
            {'brand': 'goobne', 'name': '굽네 오리지널 구이', 'product_type': 'roasted', 'tier': 'S', 'tier_score': 88},
            {'brand': 'goobne', 'name': '굽네 볼케이노 구이', 'product_type': 'roasted', 'tier': 'A', 'tier_score': 82},
            {'brand': 'bbq', 'name': 'BBQ 훈제치킨', 'product_type': 'roasted', 'tier': 'A', 'tier_score': 78},
            {'brand': 'smof', 'name': '스모프 훈제치킨', 'product_type': 'roasted', 'tier': 'B', 'tier_score': 65},
            {'brand': 'ovenmaru', 'name': '오븐마루 구이치킨', 'product_type': 'roasted', 'tier': 'B', 'tier_score': 62},

            # === 매운맛 ===
            {'brand': 'bhc', 'name': 'BHC 핫후라이드', 'product_type': 'spicy', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nene', 'name': '네네 청양마요', 'product_type': 'spicy', 'tier': 'A', 'tier_score': 80},
            {'brand': 'goobne', 'name': '굽네 고추바사삭', 'product_type': 'spicy', 'tier': 'A', 'tier_score': 78},
            {'brand': 'jicoba', 'name': '지코바 매운치킨', 'product_type': 'spicy', 'tier': 'A', 'tier_score': 75},
            {'brand': 'cheogajip', 'name': '처갓집 핫양념', 'product_type': 'spicy', 'tier': 'B', 'tier_score': 68},
            {'brand': 'pelicana', 'name': '페리카나 핫치킨', 'product_type': 'spicy', 'tier': 'B', 'tier_score': 65},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'], category=category)
                slug = f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-').replace('/', '-')}"
                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'product_type': p_data['product_type'],
                        'tier': p_data.get('tier', 'B'),
                        'tier_score': p_data['tier_score'],
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(f'    제품 추가: {product.name}')
            except Brand.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    브랜드 없음: {p_data["brand"]}'))

        self.stdout.write(self.style.SUCCESS('치킨 카테고리 업데이트 완료!'))

    def update_running_shoes(self):
        """러닝화 카테고리 - 브랜드 S~D 확장"""
        self.stdout.write('=' * 50)
        self.stdout.write('러닝화 카테고리 업데이트 중...')

        category = Category.objects.get(slug='running-shoes')

        # 1. filter_definitions 업데이트
        category.filter_definitions = {
            'product_type': [
                {'value': 'daily', 'label': '데일리 트레이너', 'description': '매일 편하게 신는 훈련화', 'icon': '👟'},
                {'value': 'race', 'label': '레이싱화', 'description': '대회/기록용 경량 슈즈', 'icon': '🏆'},
                {'value': 'tempo', 'label': '템포 러너', 'description': '속도 훈련용 슈즈', 'icon': '⚡'},
                {'value': 'cushion', 'label': '맥스 쿠션', 'description': '최대 쿠셔닝 슈즈', 'icon': '☁️'},
                {'value': 'stability', 'label': '안정화', 'description': '발목 지지력 강화 슈즈', 'icon': '🦶'},
                {'value': 'trail', 'label': '트레일', 'description': '산악/비포장 러닝화', 'icon': '🏔️'},
            ],
        }
        category.save()
        self.stdout.write('  filter_definitions 업데이트 완료')

        # 2. 브랜드 전체 정비 (S~D 티어)
        brands_data = [
            # S티어 - 러닝 전문 최상위
            {'name': '나이키', 'slug': 'nike', 'tier': 'S', 'tier_score': 95,
             'description': '알파플라이, 베이퍼플라이의 혁신 브랜드',
             'scores': {'performance': 98, 'design': 95, 'durability': 88, 'value': 70}},
            {'name': '아식스', 'slug': 'asics', 'tier': 'S', 'tier_score': 92,
             'description': 'GEL 기술의 장인, 일본 러닝화 명가',
             'scores': {'performance': 95, 'design': 82, 'durability': 95, 'value': 85}},
            {'name': '호카', 'slug': 'hoka', 'tier': 'S', 'tier_score': 90,
             'description': '맥시멀 쿠셔닝의 선구자',
             'scores': {'performance': 92, 'design': 88, 'durability': 85, 'value': 78}},

            # A티어 - 러닝 전문 상위
            {'name': '아디다스', 'slug': 'adidas', 'tier': 'A', 'tier_score': 85,
             'description': '부스트 폼의 창시자',
             'scores': {'performance': 88, 'design': 90, 'durability': 82, 'value': 80}},
            {'name': '뉴발란스', 'slug': 'new-balance', 'tier': 'A', 'tier_score': 84,
             'description': 'Fresh Foam의 편안함',
             'scores': {'performance': 85, 'design': 85, 'durability': 88, 'value': 82}},
            {'name': '브룩스', 'slug': 'brooks', 'tier': 'A', 'tier_score': 83,
             'description': '미국 러닝화 전문 브랜드',
             'scores': {'performance': 88, 'design': 75, 'durability': 90, 'value': 80}},
            {'name': '사우코니', 'slug': 'saucony', 'tier': 'A', 'tier_score': 82,
             'description': 'Endorphin 시리즈로 부활',
             'scores': {'performance': 88, 'design': 78, 'durability': 85, 'value': 82}},
            {'name': '온', 'slug': 'on', 'tier': 'A', 'tier_score': 80,
             'description': '스위스 프리미엄 러닝화',
             'scores': {'performance': 82, 'design': 92, 'durability': 78, 'value': 68}},
            {'name': '미즈노', 'slug': 'mizuno', 'tier': 'A', 'tier_score': 78,
             'description': '웨이브 기술의 일본 브랜드',
             'scores': {'performance': 82, 'design': 72, 'durability': 88, 'value': 82}},

            # B티어 - 준전문 브랜드
            {'name': '언더아머', 'slug': 'under-armour', 'tier': 'B', 'tier_score': 72,
             'description': '스포츠웨어 강자의 러닝화',
             'scores': {'performance': 75, 'design': 78, 'durability': 72, 'value': 75}},
            {'name': '퓨마', 'slug': 'puma', 'tier': 'B', 'tier_score': 70,
             'description': '니트로 폼 기술 도입',
             'scores': {'performance': 72, 'design': 80, 'durability': 68, 'value': 78}},
            {'name': '리복', 'slug': 'reebok', 'tier': 'B', 'tier_score': 68,
             'description': '피트니스 러닝화 강점',
             'scores': {'performance': 70, 'design': 72, 'durability': 70, 'value': 78}},
            {'name': '살로몬', 'slug': 'salomon', 'tier': 'B', 'tier_score': 75,
             'description': '트레일 러닝의 강자',
             'scores': {'performance': 85, 'design': 75, 'durability': 85, 'value': 70}},
            {'name': '데상트', 'slug': 'descente', 'tier': 'B', 'tier_score': 65,
             'description': '일본 스포츠 브랜드',
             'scores': {'performance': 68, 'design': 70, 'durability': 70, 'value': 72}},

            # C티어 - 캐주얼/입문용
            {'name': '스케쳐스', 'slug': 'skechers', 'tier': 'C', 'tier_score': 58,
             'description': '편안함 위주의 러닝화',
             'scores': {'performance': 55, 'design': 60, 'durability': 55, 'value': 85}},
            {'name': '프로스펙스', 'slug': 'prospecs', 'tier': 'C', 'tier_score': 52,
             'description': '국내 스포츠 브랜드',
             'scores': {'performance': 50, 'design': 55, 'durability': 55, 'value': 80}},
            {'name': '르꼬끄', 'slug': 'lecoq', 'tier': 'C', 'tier_score': 50,
             'description': '패션 스포츠 브랜드',
             'scores': {'performance': 48, 'design': 65, 'durability': 50, 'value': 72}},
            {'name': '케이스위스', 'slug': 'kswiss', 'tier': 'C', 'tier_score': 48,
             'description': '테니스 브랜드의 러닝화',
             'scores': {'performance': 45, 'design': 55, 'durability': 52, 'value': 70}},

            # D티어 - 비추천
            {'name': '휠라', 'slug': 'fila', 'tier': 'D', 'tier_score': 42,
             'description': '패션 위주, 러닝 성능 부족',
             'scores': {'performance': 35, 'design': 60, 'durability': 40, 'value': 65}},
            {'name': '르까프', 'slug': 'lecaf', 'tier': 'D', 'tier_score': 38,
             'description': '가성비 국내 브랜드',
             'scores': {'performance': 35, 'design': 45, 'durability': 40, 'value': 75}},
            {'name': '네파', 'slug': 'nepa', 'tier': 'D', 'tier_score': 35,
             'description': '아웃도어 브랜드, 러닝 전문성 부족',
             'scores': {'performance': 32, 'design': 50, 'durability': 45, 'value': 60}},
            {'name': '노스페이스', 'slug': 'northface', 'tier': 'D', 'tier_score': 40,
             'description': '아웃도어 브랜드, 러닝화 비전문',
             'scores': {'performance': 38, 'design': 55, 'durability': 50, 'value': 55}},
        ]

        for brand_data in brands_data:
            # 1. 브랜드 기본 정보만 먼저 생성/업데이트
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'description': brand_data.get('description', ''),
                    'is_active': True,
                }
            )

            # 2. BrandScore 추가
            if 'scores' in brand_data:
                for key, value in brand_data['scores'].items():
                    BrandScore.objects.update_or_create(
                        brand=brand,
                        key=key,
                        defaults={'value': value, 'label': key}
                    )

            # 3. tier와 tier_score를 직접 DB 업데이트 (save() 우회 - 마지막에 강제 설정)
            Brand.objects.filter(pk=brand.pk).update(
                tier=brand_data['tier'],
                tier_score=brand_data['tier_score']
            )

            action = '추가' if created else '업데이트'
            self.stdout.write(f'  브랜드 {action}: {brand.name} ({brand_data["tier"]}티어)')

        # 3. 제품 데이터 풍성하게
        products_data = [
            # === 데일리 트레이너 ===
            {'brand': 'nike', 'name': '페가수스 41', 'product_type': 'daily', 'tier': 'S', 'tier_score': 92},
            {'brand': 'nike', 'name': '인피니티런 4', 'product_type': 'daily', 'tier': 'A', 'tier_score': 85},
            {'brand': 'asics', 'name': '젤 님버스 26', 'product_type': 'daily', 'tier': 'S', 'tier_score': 90},
            {'brand': 'asics', 'name': '젤 컨텐드 8', 'product_type': 'daily', 'tier': 'B', 'tier_score': 72},
            {'brand': 'hoka', 'name': '클리프톤 9', 'product_type': 'daily', 'tier': 'S', 'tier_score': 92},
            {'brand': 'adidas', 'name': '울트라부스트 라이트', 'product_type': 'daily', 'tier': 'A', 'tier_score': 82},
            {'brand': 'new-balance', 'name': 'Fresh Foam 1080v13', 'product_type': 'daily', 'tier': 'A', 'tier_score': 84},
            {'brand': 'brooks', 'name': '고스트 15', 'product_type': 'daily', 'tier': 'A', 'tier_score': 82},
            {'brand': 'saucony', 'name': '라이드 17', 'product_type': 'daily', 'tier': 'A', 'tier_score': 80},
            {'brand': 'on', 'name': '클라우드몬스터', 'product_type': 'daily', 'tier': 'A', 'tier_score': 78},
            {'brand': 'mizuno', 'name': '웨이브 라이더 27', 'product_type': 'daily', 'tier': 'A', 'tier_score': 78},
            {'brand': 'under-armour', 'name': '호버 팬텀 3', 'product_type': 'daily', 'tier': 'B', 'tier_score': 70},
            {'brand': 'puma', 'name': '벨로시티 니트로 2', 'product_type': 'daily', 'tier': 'B', 'tier_score': 68},
            {'brand': 'skechers', 'name': 'GO RUN 맥스로드', 'product_type': 'daily', 'tier': 'C', 'tier_score': 55},

            # === 레이싱화 ===
            {'brand': 'nike', 'name': '알파플라이 3', 'product_type': 'race', 'tier': 'S', 'tier_score': 98},
            {'brand': 'nike', 'name': '베이퍼플라이 3', 'product_type': 'race', 'tier': 'S', 'tier_score': 96},
            {'brand': 'adidas', 'name': '아디오스 프로 3', 'product_type': 'race', 'tier': 'S', 'tier_score': 92},
            {'brand': 'asics', 'name': '메타스피드 스카이+', 'product_type': 'race', 'tier': 'S', 'tier_score': 94},
            {'brand': 'asics', 'name': '메타스피드 엣지+', 'product_type': 'race', 'tier': 'S', 'tier_score': 92},
            {'brand': 'hoka', 'name': '시엘로 X1', 'product_type': 'race', 'tier': 'A', 'tier_score': 88},
            {'brand': 'new-balance', 'name': 'SC 엘리트 v4', 'product_type': 'race', 'tier': 'A', 'tier_score': 86},
            {'brand': 'saucony', 'name': '엔돌핀 프로 4', 'product_type': 'race', 'tier': 'A', 'tier_score': 88},
            {'brand': 'brooks', 'name': '하이페리온 엘리트 4', 'product_type': 'race', 'tier': 'A', 'tier_score': 85},
            {'brand': 'puma', 'name': '파스트알-니트로 엘리트', 'product_type': 'race', 'tier': 'B', 'tier_score': 78},

            # === 템포 러너 ===
            {'brand': 'nike', 'name': '줌플라이 5', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 85},
            {'brand': 'asics', 'name': '매직스피드 3', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 82},
            {'brand': 'hoka', 'name': '맥플라이 5', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 84},
            {'brand': 'adidas', 'name': '타키안 SL', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 80},
            {'brand': 'new-balance', 'name': 'FuelCell Rebel v4', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 82},
            {'brand': 'saucony', 'name': '엔돌핀 스피드 4', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 85},
            {'brand': 'brooks', 'name': '하이페리온 템포', 'product_type': 'tempo', 'tier': 'A', 'tier_score': 80},
            {'brand': 'on', 'name': '클라우드붐 에코', 'product_type': 'tempo', 'tier': 'B', 'tier_score': 75},

            # === 맥스 쿠션 ===
            {'brand': 'hoka', 'name': '본디 8', 'product_type': 'cushion', 'tier': 'S', 'tier_score': 95},
            {'brand': 'asics', 'name': '젤 님버스 26', 'product_type': 'cushion', 'tier': 'S', 'tier_score': 92},
            {'brand': 'brooks', 'name': '글리세린 21', 'product_type': 'cushion', 'tier': 'S', 'tier_score': 88},
            {'brand': 'new-balance', 'name': 'Fresh Foam More v4', 'product_type': 'cushion', 'tier': 'A', 'tier_score': 84},
            {'brand': 'saucony', 'name': '트라이엄프 21', 'product_type': 'cushion', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nike', 'name': '인빈시블 런 3', 'product_type': 'cushion', 'tier': 'A', 'tier_score': 82},
            {'brand': 'skechers', 'name': '맥스 쿠셔닝 엘리트', 'product_type': 'cushion', 'tier': 'B', 'tier_score': 62},

            # === 안정화 ===
            {'brand': 'asics', 'name': '젤 카야노 30', 'product_type': 'stability', 'tier': 'S', 'tier_score': 92},
            {'brand': 'brooks', 'name': '아드레날린 GTS 24', 'product_type': 'stability', 'tier': 'S', 'tier_score': 88},
            {'brand': 'new-balance', 'name': 'Fresh Foam 860v14', 'product_type': 'stability', 'tier': 'A', 'tier_score': 82},
            {'brand': 'asics', 'name': 'GT-2000 12', 'product_type': 'stability', 'tier': 'A', 'tier_score': 80},
            {'brand': 'saucony', 'name': '가이드 17', 'product_type': 'stability', 'tier': 'A', 'tier_score': 78},
            {'brand': 'mizuno', 'name': '웨이브 인스파이어 20', 'product_type': 'stability', 'tier': 'A', 'tier_score': 78},
            {'brand': 'hoka', 'name': '아라히 7', 'product_type': 'stability', 'tier': 'A', 'tier_score': 80},

            # === 트레일 ===
            {'brand': 'salomon', 'name': '스피드크로스 6', 'product_type': 'trail', 'tier': 'S', 'tier_score': 92},
            {'brand': 'salomon', 'name': '울트라 글라이드 2', 'product_type': 'trail', 'tier': 'A', 'tier_score': 85},
            {'brand': 'hoka', 'name': '스피드고트 5', 'product_type': 'trail', 'tier': 'S', 'tier_score': 90},
            {'brand': 'hoka', 'name': '챌린저 7', 'product_type': 'trail', 'tier': 'A', 'tier_score': 82},
            {'brand': 'nike', 'name': '페가수스 트레일 4', 'product_type': 'trail', 'tier': 'A', 'tier_score': 78},
            {'brand': 'asics', 'name': '젤 트라부코 12', 'product_type': 'trail', 'tier': 'A', 'tier_score': 80},
            {'brand': 'new-balance', 'name': 'Fresh Foam 히에로 v7', 'product_type': 'trail', 'tier': 'B', 'tier_score': 72},
            {'brand': 'brooks', 'name': '캐스케디아 17', 'product_type': 'trail', 'tier': 'A', 'tier_score': 78},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'], category=category)
                slug = f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-').replace('/', '-')}"
                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'product_type': p_data['product_type'],
                        'tier': p_data.get('tier', 'B'),
                        'tier_score': p_data['tier_score'],
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(f'    제품 추가: {product.name}')
            except Brand.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    브랜드 없음: {p_data["brand"]}'))

        self.stdout.write(self.style.SUCCESS('러닝화 카테고리 업데이트 완료!'))

    def update_watches(self):
        """시계 카테고리 - 데이터 보강"""
        self.stdout.write('=' * 50)
        self.stdout.write('시계 카테고리 업데이트 중...')

        category = Category.objects.get(slug='mens-watch')

        # 1. filter_definitions
        category.filter_definitions = {
            'product_type': [
                {'value': 'dress', 'label': '드레스워치', 'description': '정장에 어울리는 격식있는 시계', 'icon': '👔'},
                {'value': 'sport', 'label': '스포츠워치', 'description': '활동적인 상황에 적합', 'icon': '⚽'},
                {'value': 'diver', 'label': '다이버워치', 'description': '방수 기능이 뛰어난 잠수용', 'icon': '🤿'},
                {'value': 'pilot', 'label': '파일럿워치', 'description': '항공 계기판 스타일', 'icon': '✈️'},
                {'value': 'chrono', 'label': '크로노그래프', 'description': '스톱워치 기능 탑재', 'icon': '⏱️'},
                {'value': 'field', 'label': '필드워치', 'description': '밀리터리/아웃도어 스타일', 'icon': '🏕️'},
            ],
        }
        category.save()
        self.stdout.write('  filter_definitions 업데이트 완료')

        # 2. 브랜드 전체 정비 (S~D 티어)
        brands_data = [
            # S티어 - 하이엔드 럭셔리
            {'name': '롤렉스', 'slug': 'rolex', 'tier': 'S', 'tier_score': 98,
             'description': '세계 최고의 시계 브랜드, 자산 가치까지',
             'scores': {'prestige': 100, 'quality': 98, 'resale': 100, 'design': 90}},
            {'name': '파텍필립', 'slug': 'patek-philippe', 'tier': 'S', 'tier_score': 100,
             'description': '시계계의 에르메스, 초고가 럭셔리',
             'scores': {'prestige': 100, 'quality': 100, 'resale': 98, 'design': 95}},
            {'name': '오데마피게', 'slug': 'audemars-piguet', 'tier': 'S', 'tier_score': 96,
             'description': '로얄오크의 전설',
             'scores': {'prestige': 98, 'quality': 96, 'resale': 92, 'design': 98}},
            {'name': '바쉐론콘스탄틴', 'slug': 'vacheron-constantin', 'tier': 'S', 'tier_score': 95,
             'description': '가장 오래된 시계 제조사',
             'scores': {'prestige': 98, 'quality': 98, 'resale': 85, 'design': 92}},

            # A티어 - 럭셔리
            {'name': '오메가', 'slug': 'omega', 'tier': 'A', 'tier_score': 88,
             'description': '스피드마스터, 씨마스터로 유명',
             'scores': {'prestige': 90, 'quality': 88, 'resale': 75, 'design': 88}},
            {'name': '튜더', 'slug': 'tudor', 'tier': 'A', 'tier_score': 82,
             'description': '롤렉스의 형제 브랜드',
             'scores': {'prestige': 80, 'quality': 85, 'resale': 70, 'design': 85}},
            {'name': '브라이틀링', 'slug': 'breitling', 'tier': 'A', 'tier_score': 80,
             'description': '항공 시계의 명가',
             'scores': {'prestige': 82, 'quality': 85, 'resale': 65, 'design': 82}},
            {'name': 'IWC', 'slug': 'iwc', 'tier': 'A', 'tier_score': 82,
             'description': '포르투기저, 파일럿 시리즈',
             'scores': {'prestige': 85, 'quality': 88, 'resale': 68, 'design': 85}},
            {'name': '까르띠에', 'slug': 'cartier', 'tier': 'A', 'tier_score': 85,
             'description': '탱크, 산토스 등 아이코닉 디자인',
             'scores': {'prestige': 90, 'quality': 82, 'resale': 72, 'design': 95}},
            {'name': '그랜드세이코', 'slug': 'grand-seiko', 'tier': 'A', 'tier_score': 78,
             'description': '일본 장인정신의 결정체',
             'scores': {'prestige': 75, 'quality': 95, 'resale': 60, 'design': 80}},

            # B티어 - 프리미엄
            {'name': '태그호이어', 'slug': 'tag-heuer', 'tier': 'B', 'tier_score': 72,
             'description': '레이싱 시계의 아이콘',
             'scores': {'prestige': 72, 'quality': 75, 'resale': 55, 'design': 78}},
            {'name': '론진', 'slug': 'longines', 'tier': 'B', 'tier_score': 70,
             'description': '스와치 그룹의 클래식 브랜드',
             'scores': {'prestige': 70, 'quality': 78, 'resale': 50, 'design': 75}},
            {'name': '오리스', 'slug': 'oris', 'tier': 'B', 'tier_score': 68,
             'description': '스위스 독립 시계 브랜드',
             'scores': {'prestige': 65, 'quality': 78, 'resale': 52, 'design': 72}},
            {'name': '세이코', 'slug': 'seiko', 'tier': 'B', 'tier_score': 65,
             'description': '일본 시계의 자존심',
             'scores': {'prestige': 58, 'quality': 82, 'resale': 45, 'design': 70}},
            {'name': '해밀턴', 'slug': 'hamilton', 'tier': 'B', 'tier_score': 68,
             'description': '미국 헤리티지, 스위스 품질',
             'scores': {'prestige': 62, 'quality': 75, 'resale': 48, 'design': 78}},
            {'name': '티쏘', 'slug': 'tissot', 'tier': 'B', 'tier_score': 62,
             'description': '가성비 스위스 시계',
             'scores': {'prestige': 55, 'quality': 72, 'resale': 42, 'design': 68}},

            # C티어 - 입문용
            {'name': '오리엔트', 'slug': 'orient', 'tier': 'C', 'tier_score': 55,
             'description': '가성비 일본 기계식 시계',
             'scores': {'prestige': 45, 'quality': 68, 'resale': 35, 'design': 62}},
            {'name': '시티즌', 'slug': 'citizen', 'tier': 'C', 'tier_score': 52,
             'description': '에코드라이브 솔라 시계',
             'scores': {'prestige': 48, 'quality': 65, 'resale': 30, 'design': 58}},
            {'name': '카시오', 'slug': 'casio', 'tier': 'C', 'tier_score': 50,
             'description': 'G-SHOCK의 본좌',
             'scores': {'prestige': 40, 'quality': 70, 'resale': 35, 'design': 55}},
            {'name': '스와치', 'slug': 'swatch', 'tier': 'C', 'tier_score': 48,
             'description': '컬러풀한 패션 시계',
             'scores': {'prestige': 42, 'quality': 55, 'resale': 25, 'design': 72}},
            {'name': '빅토리녹스', 'slug': 'victorinox', 'tier': 'C', 'tier_score': 52,
             'description': '스위스 아미나이프 브랜드',
             'scores': {'prestige': 48, 'quality': 65, 'resale': 30, 'design': 58}},

            # D티어 - 패션/비추천
            {'name': '다니엘웰링턴', 'slug': 'daniel-wellington', 'tier': 'D', 'tier_score': 35,
             'description': 'SNS 마케팅 패션 시계',
             'scores': {'prestige': 25, 'quality': 35, 'resale': 15, 'design': 60}},
            {'name': 'MVMT', 'slug': 'mvmt', 'tier': 'D', 'tier_score': 32,
             'description': '크라우드펀딩 출신 패션 시계',
             'scores': {'prestige': 22, 'quality': 32, 'resale': 10, 'design': 55}},
            {'name': '포슬', 'slug': 'fossil', 'tier': 'D', 'tier_score': 40,
             'description': '패션 브랜드 라이선스',
             'scores': {'prestige': 32, 'quality': 42, 'resale': 20, 'design': 55}},
            {'name': '아르마니', 'slug': 'emporio-armani', 'tier': 'D', 'tier_score': 38,
             'description': '패션 브랜드 라이선스',
             'scores': {'prestige': 35, 'quality': 38, 'resale': 18, 'design': 58}},
            {'name': '디젤', 'slug': 'diesel', 'tier': 'D', 'tier_score': 35,
             'description': '대형 케이스 패션 시계',
             'scores': {'prestige': 28, 'quality': 35, 'resale': 15, 'design': 52}},
        ]

        for brand_data in brands_data:
            # 1. 브랜드 기본 정보만 먼저 생성/업데이트
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'description': brand_data.get('description', ''),
                    'is_active': True,
                }
            )

            # 2. BrandScore 추가
            if 'scores' in brand_data:
                for key, value in brand_data['scores'].items():
                    BrandScore.objects.update_or_create(
                        brand=brand,
                        key=key,
                        defaults={'value': value, 'label': key}
                    )

            # 3. tier와 tier_score를 직접 DB 업데이트 (save() 우회 - 마지막에 강제 설정)
            Brand.objects.filter(pk=brand.pk).update(
                tier=brand_data['tier'],
                tier_score=brand_data['tier_score']
            )

            action = '추가' if created else '업데이트'
            self.stdout.write(f'  브랜드 {action}: {brand.name} ({brand_data["tier"]}티어)')

        # 3. 제품 데이터
        products_data = [
            # === 드레스워치 ===
            {'brand': 'patek-philippe', 'name': '칼라트라바 5196', 'product_type': 'dress', 'tier': 'S', 'tier_score': 98},
            {'brand': 'vacheron-constantin', 'name': '패트리모니', 'product_type': 'dress', 'tier': 'S', 'tier_score': 95},
            {'brand': 'rolex', 'name': '데이트저스트 41', 'product_type': 'dress', 'tier': 'S', 'tier_score': 92},
            {'brand': 'omega', 'name': '드빌 프레스티지', 'product_type': 'dress', 'tier': 'A', 'tier_score': 82},
            {'brand': 'cartier', 'name': '탱크 프랑세즈', 'product_type': 'dress', 'tier': 'A', 'tier_score': 88},
            {'brand': 'grand-seiko', 'name': 'SBGW231', 'product_type': 'dress', 'tier': 'A', 'tier_score': 78},
            {'brand': 'longines', 'name': '마스터 컬렉션', 'product_type': 'dress', 'tier': 'B', 'tier_score': 68},
            {'brand': 'tissot', 'name': '르로끌 파워매틱', 'product_type': 'dress', 'tier': 'B', 'tier_score': 62},
            {'brand': 'orient', 'name': '뱀비노', 'product_type': 'dress', 'tier': 'C', 'tier_score': 52},
            {'brand': 'seiko', 'name': '프레사지 칵테일', 'product_type': 'dress', 'tier': 'B', 'tier_score': 65},

            # === 다이버워치 ===
            {'brand': 'rolex', 'name': '서브마리너 데이트', 'product_type': 'diver', 'tier': 'S', 'tier_score': 98},
            {'brand': 'rolex', 'name': '씨드웰러', 'product_type': 'diver', 'tier': 'S', 'tier_score': 95},
            {'brand': 'omega', 'name': '씨마스터 300M', 'product_type': 'diver', 'tier': 'A', 'tier_score': 88},
            {'brand': 'omega', 'name': '씨마스터 플래닛오션', 'product_type': 'diver', 'tier': 'A', 'tier_score': 85},
            {'brand': 'tudor', 'name': '블랙베이 58', 'product_type': 'diver', 'tier': 'A', 'tier_score': 82},
            {'brand': 'tudor', 'name': '페라고스', 'product_type': 'diver', 'tier': 'A', 'tier_score': 80},
            {'brand': 'oris', 'name': '아퀴스 데이트', 'product_type': 'diver', 'tier': 'B', 'tier_score': 68},
            {'brand': 'seiko', 'name': '프로스펙스 SPB143', 'product_type': 'diver', 'tier': 'B', 'tier_score': 65},
            {'brand': 'orient', 'name': '카마스', 'product_type': 'diver', 'tier': 'C', 'tier_score': 52},
            {'brand': 'citizen', 'name': '프로마스터 다이버', 'product_type': 'diver', 'tier': 'C', 'tier_score': 50},

            # === 스포츠워치 ===
            {'brand': 'rolex', 'name': '데이토나', 'product_type': 'sport', 'tier': 'S', 'tier_score': 100},
            {'brand': 'rolex', 'name': '익스플로러 II', 'product_type': 'sport', 'tier': 'S', 'tier_score': 92},
            {'brand': 'audemars-piguet', 'name': '로얄오크', 'product_type': 'sport', 'tier': 'S', 'tier_score': 98},
            {'brand': 'patek-philippe', 'name': '노틸러스 5711', 'product_type': 'sport', 'tier': 'S', 'tier_score': 100},
            {'brand': 'omega', 'name': '스피드마스터 문워치', 'product_type': 'sport', 'tier': 'A', 'tier_score': 88},
            {'brand': 'tag-heuer', 'name': '카레라', 'product_type': 'sport', 'tier': 'B', 'tier_score': 72},
            {'brand': 'tag-heuer', 'name': '모나코', 'product_type': 'sport', 'tier': 'B', 'tier_score': 75},
            {'brand': 'tissot', 'name': 'PRX 파워매틱', 'product_type': 'sport', 'tier': 'B', 'tier_score': 65},
            {'brand': 'casio', 'name': 'G-SHOCK GA-2100', 'product_type': 'sport', 'tier': 'C', 'tier_score': 55},
            {'brand': 'casio', 'name': 'G-SHOCK DW-5600', 'product_type': 'sport', 'tier': 'C', 'tier_score': 52},

            # === 파일럿워치 ===
            {'brand': 'iwc', 'name': '빅파일럿', 'product_type': 'pilot', 'tier': 'A', 'tier_score': 88},
            {'brand': 'iwc', 'name': '마크 XX', 'product_type': 'pilot', 'tier': 'A', 'tier_score': 82},
            {'brand': 'breitling', 'name': '나비타이머', 'product_type': 'pilot', 'tier': 'A', 'tier_score': 85},
            {'brand': 'breitling', 'name': '슈퍼오션 헤리티지', 'product_type': 'pilot', 'tier': 'A', 'tier_score': 80},
            {'brand': 'hamilton', 'name': '카키 파일럿', 'product_type': 'pilot', 'tier': 'B', 'tier_score': 68},
            {'brand': 'seiko', 'name': '프로스펙스 플라이트마스터', 'product_type': 'pilot', 'tier': 'B', 'tier_score': 62},

            # === 필드워치 ===
            {'brand': 'rolex', 'name': '익스플로러 I', 'product_type': 'field', 'tier': 'S', 'tier_score': 92},
            {'brand': 'tudor', 'name': '레인저', 'product_type': 'field', 'tier': 'A', 'tier_score': 78},
            {'brand': 'hamilton', 'name': '카키 필드', 'product_type': 'field', 'tier': 'B', 'tier_score': 70},
            {'brand': 'hamilton', 'name': '카키 필드 메카니컬', 'product_type': 'field', 'tier': 'B', 'tier_score': 68},
            {'brand': 'seiko', 'name': '알피니스트 SPB117', 'product_type': 'field', 'tier': 'B', 'tier_score': 65},
            {'brand': 'casio', 'name': 'PRO TREK', 'product_type': 'field', 'tier': 'C', 'tier_score': 52},

            # === 크로노그래프 ===
            {'brand': 'rolex', 'name': '코스모그래프 데이토나', 'product_type': 'chrono', 'tier': 'S', 'tier_score': 100},
            {'brand': 'omega', 'name': '스피드마스터 프로페셔널', 'product_type': 'chrono', 'tier': 'A', 'tier_score': 90},
            {'brand': 'tag-heuer', 'name': '카레라 크로노', 'product_type': 'chrono', 'tier': 'B', 'tier_score': 72},
            {'brand': 'breitling', 'name': '크로노맷', 'product_type': 'chrono', 'tier': 'A', 'tier_score': 78},
            {'brand': 'tissot', 'name': 'PRS 516 크로노그래프', 'product_type': 'chrono', 'tier': 'B', 'tier_score': 60},
            {'brand': 'seiko', 'name': '프로스펙스 스피드타이머', 'product_type': 'chrono', 'tier': 'B', 'tier_score': 62},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'], category=category)
                slug = f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-').replace('/', '-')}"
                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'product_type': p_data['product_type'],
                        'tier': p_data.get('tier', 'B'),
                        'tier_score': p_data['tier_score'],
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(f'    제품 추가: {product.name}')
            except Brand.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    브랜드 없음: {p_data["brand"]}'))

        self.stdout.write(self.style.SUCCESS('시계 카테고리 업데이트 완료!'))
