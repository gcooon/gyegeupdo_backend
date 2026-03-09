"""
용도별 계급도 데이터 대량 업데이트 커맨드
- filter_definitions 개선
- 브랜드 티어 확장 (S~D)
- 제품 usage 데이터 보강
"""
from django.core.management.base import BaseCommand
from brands.models import Category, Brand, BrandScore
from models_app.models import Product, ProductScore


class Command(BaseCommand):
    help = '용도별 계급도 데이터 업데이트'

    def handle(self, *args, **options):
        self.update_running_shoes()
        self.update_chicken()
        self.update_watches()
        self.stdout.write(self.style.SUCCESS('데이터 업데이트 완료!'))

    def update_running_shoes(self):
        """러닝화 카테고리 업데이트"""
        self.stdout.write('러닝화 카테고리 업데이트 중...')

        category = Category.objects.get(slug='running-shoes')

        # 1. filter_definitions 개선
        category.filter_definitions = {
            'product_type': [
                {'value': 'cushion', 'label': '쿠셔닝', 'description': '충격 흡수가 뛰어난 편안한 러닝화', 'icon': '☁️'},
                {'value': 'stability', 'label': '안정화', 'description': '발목 지지력이 좋은 안정적인 러닝화', 'icon': '🦶'},
                {'value': 'speed', 'label': '스피드', 'description': '가볍고 빠른 레이싱용 러닝화', 'icon': '⚡'},
                {'value': 'trail', 'label': '트레일', 'description': '산악/비포장 도로용 러닝화', 'icon': '🏔️'},
            ],
            'usage': [
                {'value': 'beginner', 'label': '입문/조깅', 'description': '처음 러닝을 시작하는 분께 추천', 'icon': '🌱'},
                {'value': 'daily', 'label': '데일리 트레이닝', 'description': '매일 편하게 신을 수 있는 훈련화', 'icon': '📅'},
                {'value': 'tempo', 'label': '템포/인터벌', 'description': '속도 훈련용 러닝화', 'icon': '⏱️'},
                {'value': 'race', 'label': '레이스/마라톤', 'description': '대회 및 기록 단축용', 'icon': '🏆'},
                {'value': 'long', 'label': '장거리/LSD', 'description': '장거리 훈련용 러닝화', 'icon': '🛤️'},
                {'value': 'recovery', 'label': '회복/조깅', 'description': '가볍게 뛸 때 신는 편안한 러닝화', 'icon': '🧘'},
            ]
        }
        category.save()

        # 2. 브랜드 추가 (B, C, D 티어)
        new_brands = [
            # B티어 브랜드
            {'name': '언더아머', 'slug': 'under-armour', 'tier': 'B', 'tier_score': 72,
             'description': '스포츠웨어 강자, 러닝화도 준수한 성능'},
            {'name': '리복', 'slug': 'reebok', 'tier': 'B', 'tier_score': 68,
             'description': '크로스핏과 피트니스 러닝화로 유명'},
            {'name': '살로몬', 'slug': 'salomon', 'tier': 'B', 'tier_score': 75,
             'description': '트레일 러닝의 강자'},
            # C티어 브랜드
            {'name': '스케쳐스', 'slug': 'skechers', 'tier': 'C', 'tier_score': 58,
             'description': '편안함 위주의 가성비 러닝화'},
            {'name': '프로스펙스', 'slug': 'prospecs', 'tier': 'C', 'tier_score': 52,
             'description': '국내 스포츠 브랜드'},
            {'name': '데상트', 'slug': 'descente', 'tier': 'C', 'tier_score': 55,
             'description': '일본 스포츠 브랜드'},
            # D티어 브랜드
            {'name': '휠라', 'slug': 'fila', 'tier': 'D', 'tier_score': 42,
             'description': '패션 위주, 본격 러닝용으로는 부족'},
            {'name': '르까프', 'slug': 'lecaf', 'tier': 'D', 'tier_score': 38,
             'description': '가성비 위주 국내 브랜드'},
            {'name': '네파', 'slug': 'nepa', 'tier': 'D', 'tier_score': 35,
             'description': '아웃도어 브랜드, 전문 러닝화 부족'},
        ]

        for brand_data in new_brands:
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'tier': brand_data['tier'],
                    'tier_score': brand_data['tier_score'],
                    'description': brand_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  브랜드 추가: {brand.name}')

        # 3. 제품 추가 (용도별로 균형있게)
        products_data = [
            # 입문/조깅용
            {'brand': 'asics', 'name': 'GEL-CONTEND 8', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 72},
            {'brand': 'nike', 'name': 'Revolution 7', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 70},
            {'brand': 'adidas', 'name': 'Galaxy 7', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 68},
            {'brand': 'new-balance', 'name': 'Fresh Foam 680v8', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 71},
            {'brand': 'skechers', 'name': 'GO RUN Lite', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 58},
            {'brand': 'skechers', 'name': 'Max Cushioning Elite', 'usage': 'beginner', 'type': 'cushion', 'tier_score': 62},
            # 장거리/LSD용
            {'brand': 'asics', 'name': 'GEL-NIMBUS 26', 'usage': 'long', 'type': 'cushion', 'tier_score': 88},
            {'brand': 'nike', 'name': 'InfinityRN 4', 'usage': 'long', 'type': 'cushion', 'tier_score': 85},
            {'brand': 'hoka', 'name': 'Bondi 8', 'usage': 'long', 'type': 'cushion', 'tier_score': 90},
            {'brand': 'new-balance', 'name': 'Fresh Foam More v4', 'usage': 'long', 'type': 'cushion', 'tier_score': 84},
            {'brand': 'brooks', 'name': 'Glycerin 21', 'usage': 'long', 'type': 'cushion', 'tier_score': 87},
            {'brand': 'saucony', 'name': 'Triumph 21', 'usage': 'long', 'type': 'cushion', 'tier_score': 86},
            # 회복/조깅용
            {'brand': 'hoka', 'name': 'Clifton 9', 'usage': 'recovery', 'type': 'cushion', 'tier_score': 88},
            {'brand': 'on', 'name': 'Cloudmonster', 'usage': 'recovery', 'type': 'cushion', 'tier_score': 82},
            {'brand': 'asics', 'name': 'GEL-KAYANO 30', 'usage': 'recovery', 'type': 'stability', 'tier_score': 86},
            {'brand': 'brooks', 'name': 'Ghost 15', 'usage': 'recovery', 'type': 'cushion', 'tier_score': 84},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'])
                product, created = Product.objects.update_or_create(
                    slug=f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-')}",
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'usage': p_data['usage'],
                        'product_type': p_data['type'],
                        'tier_score': p_data['tier_score'],
                    }
                )
                if created:
                    self.stdout.write(f'  제품 추가: {product.name}')
            except Brand.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('러닝화 업데이트 완료'))

    def update_chicken(self):
        """치킨 카테고리 업데이트"""
        self.stdout.write('치킨 카테고리 업데이트 중...')

        category = Category.objects.get(slug='chicken')

        # 1. filter_definitions 개선
        category.filter_definitions = {
            'product_type': [
                {'value': 'fried', 'label': '후라이드', 'description': '바삭한 기본 후라이드 치킨', 'icon': '🍗'},
                {'value': 'seasoned', 'label': '양념', 'description': '달콤 매콤한 양념 치킨', 'icon': '🌶️'},
                {'value': 'soy', 'label': '간장', 'description': '짭짤한 간장 소스 치킨', 'icon': '🥢'},
                {'value': 'cheese', 'label': '치즈', 'description': '치즈 토핑 또는 치즈 시즈닝', 'icon': '🧀'},
                {'value': 'garlic', 'label': '마늘', 'description': '마늘 풍미가 강한 치킨', 'icon': '🧄'},
                {'value': 'roasted', 'label': '구이', 'description': '오븐/숯불 구이 치킨', 'icon': '🔥'},
            ],
            'usage': [
                {'value': 'solo', 'label': '혼닭', 'description': '혼자 먹기 좋은 치킨', 'icon': '🙋'},
                {'value': 'beer', 'label': '치맥', 'description': '맥주와 찰떡궁합', 'icon': '🍺'},
                {'value': 'family', 'label': '가족/모임', 'description': '여러 명이 함께 먹기 좋은', 'icon': '👨‍👩‍👧‍👦'},
                {'value': 'latenight', 'label': '야식', 'description': '늦은 밤 출출할 때', 'icon': '🌙'},
                {'value': 'value', 'label': '가성비', 'description': '가격 대비 양이 푸짐한', 'icon': '💰'},
                {'value': 'diet', 'label': '다이어트', 'description': '칼로리 걱정 적은 치킨', 'icon': '🥗'},
            ]
        }
        category.save()

        # 2. 브랜드 추가 (B, C, D 티어)
        new_brands = [
            # B티어 - 중견 프랜차이즈
            {'name': '처갓집양념치킨', 'slug': 'cheogajip', 'tier': 'B', 'tier_score': 72,
             'scores': {'taste': 75, 'price': 78, 'crispy': 70, 'popularity': 72}},
            {'name': '페리카나', 'slug': 'pelicana', 'tier': 'B', 'tier_score': 70,
             'scores': {'taste': 72, 'price': 80, 'crispy': 68, 'popularity': 65}},
            {'name': '호식이두마리치킨', 'slug': 'hosigi', 'tier': 'B', 'tier_score': 74,
             'scores': {'taste': 70, 'price': 90, 'crispy': 72, 'popularity': 75}},
            {'name': '자담치킨', 'slug': 'jadam', 'tier': 'B', 'tier_score': 68,
             'scores': {'taste': 72, 'price': 75, 'crispy': 65, 'popularity': 60}},
            # C티어 - 소형/가성비 프랜차이즈
            {'name': '60계치킨', 'slug': '60gye', 'tier': 'C', 'tier_score': 58,
             'scores': {'taste': 55, 'price': 92, 'crispy': 55, 'popularity': 50}},
            {'name': '노랑통닭', 'slug': 'norang', 'tier': 'C', 'tier_score': 55,
             'scores': {'taste': 58, 'price': 88, 'crispy': 52, 'popularity': 45}},
            {'name': '또래오래', 'slug': 'ttorae', 'tier': 'C', 'tier_score': 52,
             'scores': {'taste': 52, 'price': 90, 'crispy': 50, 'popularity': 40}},
            {'name': '땅땅치킨', 'slug': 'ddangddang', 'tier': 'C', 'tier_score': 50,
             'scores': {'taste': 50, 'price': 92, 'crispy': 48, 'popularity': 38}},
            # D티어 - 비추천
            {'name': '편의점치킨', 'slug': 'convenience', 'tier': 'D', 'tier_score': 35,
             'scores': {'taste': 35, 'price': 65, 'crispy': 25, 'popularity': 30}},
            {'name': '마트델리치킨', 'slug': 'mart-deli', 'tier': 'D', 'tier_score': 38,
             'scores': {'taste': 40, 'price': 75, 'crispy': 30, 'popularity': 35}},
            {'name': '냉동치킨', 'slug': 'frozen', 'tier': 'D', 'tier_score': 32,
             'scores': {'taste': 32, 'price': 70, 'crispy': 25, 'popularity': 28}},
        ]

        for brand_data in new_brands:
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'tier': brand_data['tier'],
                    'tier_score': brand_data['tier_score'],
                }
            )
            # BrandScore 추가
            if 'scores' in brand_data:
                for key, value in brand_data['scores'].items():
                    BrandScore.objects.update_or_create(
                        brand=brand,
                        key=key,
                        defaults={'value': value}
                    )
            if created:
                self.stdout.write(f'  브랜드 추가: {brand.name}')

        # 3. 제품 추가 (용도별로 균형있게)
        products_data = [
            # 혼닭용
            {'brand': 'bbq', 'name': '황금올리브 반마리', 'usage': 'solo', 'type': 'fried', 'tier_score': 85},
            {'brand': 'kyochon', 'name': '교촌 허니콤보 반마리', 'usage': 'solo', 'type': 'soy', 'tier_score': 82},
            {'brand': 'hosigi', 'name': '호식이 한마리', 'usage': 'solo', 'type': 'fried', 'tier_score': 75},
            {'brand': '60gye', 'name': '60계 한마리', 'usage': 'solo', 'type': 'fried', 'tier_score': 55},
            # 야식용
            {'brand': 'bhc', 'name': '뿌링클', 'usage': 'latenight', 'type': 'cheese', 'tier_score': 88},
            {'brand': 'goobne', 'name': '굽네 볼케이노', 'usage': 'latenight', 'type': 'roasted', 'tier_score': 78},
            {'brand': 'nene', 'name': '네네 스노윙', 'usage': 'latenight', 'type': 'cheese', 'tier_score': 80},
            {'brand': 'pelicana', 'name': '양념치킨', 'usage': 'latenight', 'type': 'seasoned', 'tier_score': 70},
            # 가성비용
            {'brand': 'hosigi', 'name': '두마리치킨 세트', 'usage': 'value', 'type': 'fried', 'tier_score': 78},
            {'brand': '60gye', 'name': '후라이드+양념 세트', 'usage': 'value', 'type': 'fried', 'tier_score': 58},
            {'brand': 'norang', 'name': '통닭 세트', 'usage': 'value', 'type': 'fried', 'tier_score': 55},
            {'brand': 'ttorae', 'name': '순살세트', 'usage': 'value', 'type': 'fried', 'tier_score': 52},
            # 다이어트용
            {'brand': 'goobne', 'name': '굽네 오리지널', 'usage': 'diet', 'type': 'roasted', 'tier_score': 82},
            {'brand': 'goobne', 'name': '굽네 고추바사삭', 'usage': 'diet', 'type': 'roasted', 'tier_score': 80},
            {'brand': 'bbq', 'name': '자메이카 소떡만나', 'usage': 'diet', 'type': 'roasted', 'tier_score': 75},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'])
                product, created = Product.objects.update_or_create(
                    slug=f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-')}",
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'usage': p_data['usage'],
                        'product_type': p_data['type'],
                        'tier_score': p_data['tier_score'],
                    }
                )
                if created:
                    self.stdout.write(f'  제품 추가: {product.name}')
            except Brand.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('치킨 업데이트 완료'))

    def update_watches(self):
        """시계 카테고리 업데이트"""
        self.stdout.write('시계 카테고리 업데이트 중...')

        category = Category.objects.get(slug='mens-watch')

        # 1. filter_definitions 개선
        category.filter_definitions = {
            'product_type': [
                {'value': 'dress', 'label': '드레스워치', 'description': '격식있는 자리에 어울리는 시계', 'icon': '👔'},
                {'value': 'sport', 'label': '스포츠워치', 'description': '활동적인 상황에 적합한 시계', 'icon': '⚽'},
                {'value': 'diver', 'label': '다이버워치', 'description': '방수 기능이 뛰어난 잠수용 시계', 'icon': '🤿'},
                {'value': 'pilot', 'label': '파일럿워치', 'description': '항공 계기판 스타일의 시계', 'icon': '✈️'},
                {'value': 'chrono', 'label': '크로노그래프', 'description': '스톱워치 기능이 있는 시계', 'icon': '⏱️'},
            ],
            'usage': [
                {'value': 'daily', 'label': '데일리', 'description': '일상에서 매일 착용', 'icon': '☀️'},
                {'value': 'formal', 'label': '포멀/비즈니스', 'description': '정장과 어울리는 격식있는 시계', 'icon': '💼'},
                {'value': 'casual', 'label': '캐주얼', 'description': '편하게 착용하는 시계', 'icon': '👕'},
                {'value': 'sport', 'label': '스포츠/아웃도어', 'description': '운동 및 야외 활동용', 'icon': '🏃'},
                {'value': 'luxury', 'label': '컬렉션/투자', 'description': '소장 가치가 높은 시계', 'icon': '💎'},
                {'value': 'entry', 'label': '입문/첫시계', 'description': '시계 입문자에게 추천', 'icon': '🌱'},
            ]
        }
        category.save()

        # 2. D티어 브랜드 추가
        new_brands = [
            {'name': '다니엘웰링턴', 'slug': 'daniel-wellington', 'tier': 'D', 'tier_score': 35,
             'description': '패션 시계, 무브먼트 품질 낮음'},
            {'name': 'MVMT', 'slug': 'mvmt', 'tier': 'D', 'tier_score': 32,
             'description': 'SNS 마케팅 위주, 품질 대비 고가'},
            {'name': '포슬', 'slug': 'fossil', 'tier': 'D', 'tier_score': 40,
             'description': '패션 시계, 무브먼트 저가'},
            {'name': '알마니 익스체인지', 'slug': 'armani-exchange', 'tier': 'D', 'tier_score': 38,
             'description': '패션 브랜드 라이선스 시계'},
        ]

        for brand_data in new_brands:
            brand, created = Brand.objects.update_or_create(
                slug=brand_data['slug'],
                defaults={
                    'category': category,
                    'name': brand_data['name'],
                    'tier': brand_data['tier'],
                    'tier_score': brand_data['tier_score'],
                    'description': brand_data.get('description', ''),
                }
            )
            if created:
                self.stdout.write(f'  브랜드 추가: {brand.name}')

        # 3. 입문용 제품 추가
        products_data = [
            {'brand': 'seiko', 'name': 'Presage Cocktail', 'usage': 'entry', 'type': 'dress', 'tier_score': 72},
            {'brand': 'orient', 'name': 'Bambino', 'usage': 'entry', 'type': 'dress', 'tier_score': 65},
            {'brand': 'tissot', 'name': 'PRX', 'usage': 'entry', 'type': 'sport', 'tier_score': 70},
            {'brand': 'hamilton', 'name': 'Khaki Field', 'usage': 'entry', 'type': 'pilot', 'tier_score': 72},
            {'brand': 'casio', 'name': 'G-SHOCK GA-2100', 'usage': 'entry', 'type': 'sport', 'tier_score': 60},
            # 데일리용
            {'brand': 'tudor', 'name': 'Black Bay 58', 'usage': 'daily', 'type': 'diver', 'tier_score': 85},
            {'brand': 'omega', 'name': 'Seamaster 300M', 'usage': 'daily', 'type': 'diver', 'tier_score': 88},
            {'brand': 'rolex', 'name': 'Explorer', 'usage': 'daily', 'type': 'sport', 'tier_score': 92},
        ]

        for p_data in products_data:
            try:
                brand = Brand.objects.get(slug=p_data['brand'])
                product, created = Product.objects.update_or_create(
                    slug=f"{p_data['brand']}-{p_data['name'].lower().replace(' ', '-')}",
                    defaults={
                        'brand': brand,
                        'category': category,
                        'name': p_data['name'],
                        'usage': p_data['usage'],
                        'product_type': p_data['type'],
                        'tier_score': p_data['tier_score'],
                    }
                )
                if created:
                    self.stdout.write(f'  제품 추가: {product.name}')
            except Brand.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('시계 업데이트 완료'))
