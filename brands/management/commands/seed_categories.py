"""
카테고리 및 브랜드 시드 데이터 생성 커맨드.
사용: python manage.py seed_categories
"""
from django.core.management.base import BaseCommand
from brands.models import Category, Brand, BrandScore


def favicon_url(domain):
    return f'https://www.google.com/s2/favicons?domain={domain}&sz=128'


CATEGORIES_DATA = [
    {
        'name': '러닝화',
        'slug': 'running-shoes',
        'icon': '👟',
        'description': '러닝화 브랜드 계급도 - 커뮤니티 리뷰 기반',
        'display_order': 1,
        'display_config': {
            'color': '#E94560',
            'heroTitle': '러닝화 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 리뷰를 바탕으로 S~B 티어로 분류된 러닝화 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 러닝화 찾기',
            'stats': {'modelCount': '40+', 'reviewCount': '2,500+', 'brandCount': '15'},
        },
        'brand_score_definitions': [
            {'key': 'lineup', 'label': '라인업', 'weight': 25},
            {'key': 'tech', 'label': '기술력', 'weight': 30},
            {'key': 'durability', 'label': '내구성', 'weight': 25},
            {'key': 'community', 'label': '커뮤니티', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'cushion', 'label': '쿠셔닝', 'weight': 25},
            {'key': 'responsiveness', 'label': '반응성', 'weight': 25},
            {'key': 'stability', 'label': '안정성', 'weight': 25},
            {'key': 'durability', 'label': '내구성', 'weight': 25},
        ],
        'spec_definitions': [
            {'key': 'weight', 'label': '무게', 'unit': 'g', 'type': 'number'},
            {'key': 'stack_height', 'label': '스택 높이', 'unit': 'mm', 'type': 'number'},
            {'key': 'drop', 'label': '드롭', 'unit': 'mm', 'type': 'number'},
            {'key': 'upper', 'label': '어퍼 소재', 'type': 'text'},
            {'key': 'midsole', 'label': '미드솔', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'cushion', 'label': '쿠션화'},
                {'value': 'stability', 'label': '안정화'},
                {'value': 'speed', 'label': '스피드'},
                {'value': 'trail', 'label': '트레일'},
            ],
            'usage': [
                {'value': 'beginner', 'label': '입문'},
                {'value': 'daily', 'label': '데일리'},
                {'value': 'tempo', 'label': '템포'},
                {'value': 'race', 'label': '레이스'},
            ],
        },
        'brands': [
            {'name': '아식스', 'slug': 'asics', 'domain': 'asics.com', 'description': '일본의 러닝화 명가, 젤 쿠셔닝 기술의 선두주자', 'scores': {'lineup': 96, 'tech': 97, 'durability': 95, 'community': 92}},
            {'name': '나이키', 'slug': 'nike', 'domain': 'nike.com', 'description': '세계 최대 스포츠 브랜드, 혁신적인 기술력', 'scores': {'lineup': 98, 'tech': 96, 'durability': 88, 'community': 95}},
            {'name': '호카', 'slug': 'hoka', 'domain': 'hoka.com', 'description': '맥시멀 쿠셔닝의 혁명, 편안함의 대명사', 'scores': {'lineup': 88, 'tech': 94, 'durability': 90, 'community': 96}},
            {'name': '뉴발란스', 'slug': 'new-balance', 'domain': 'newbalance.com', 'description': '프레시폼 기술의 선두, 안정성과 편안함', 'scores': {'lineup': 90, 'tech': 88, 'durability': 89, 'community': 85}},
            {'name': '써코니', 'slug': 'saucony', 'domain': 'saucony.com', 'description': '러너들의 러너, PWRRUN 쿠셔닝 기술', 'scores': {'lineup': 85, 'tech': 90, 'durability': 88, 'community': 84}},
            {'name': '브룩스', 'slug': 'brooks', 'domain': 'brooksrunning.com', 'description': 'DNA 쿠셔닝 기술, 안정화의 명가', 'scores': {'lineup': 82, 'tech': 88, 'durability': 90, 'community': 80}},
            {'name': '아디다스', 'slug': 'adidas', 'domain': 'adidas.com', 'description': '부스트 기술의 창시자, 스타일과 성능의 조화', 'scores': {'lineup': 88, 'tech': 85, 'durability': 80, 'community': 82}},
            {'name': '푸마', 'slug': 'puma', 'domain': 'puma.com', 'description': 'NITRO 폼의 혁신, 가성비 좋은 퍼포먼스', 'scores': {'lineup': 78, 'tech': 82, 'durability': 78, 'community': 75}},
            {'name': '온러닝', 'slug': 'on-running', 'domain': 'on-running.com', 'description': '스위스 기술의 CloudTec, 독특한 쿠셔닝', 'scores': {'lineup': 72, 'tech': 80, 'durability': 75, 'community': 78}},
            {'name': '미즈노', 'slug': 'mizuno', 'domain': 'mizuno.com', 'description': '웨이브 플레이트 기술, 일본 장인 정신', 'scores': {'lineup': 70, 'tech': 78, 'durability': 82, 'community': 65}},
            {'name': '리복', 'slug': 'reebok', 'domain': 'reebok.com', 'description': '플로트라이드 기술, 가성비 러닝화', 'scores': {'lineup': 55, 'tech': 60, 'durability': 62, 'community': 48}},
            {'name': '스케쳐스', 'slug': 'skechers', 'domain': 'skechers.com', 'description': '편안함의 대명사, 넓은 라인업', 'scores': {'lineup': 65, 'tech': 55, 'durability': 58, 'community': 50}},
        ],
    },
    {
        'name': '치킨',
        'slug': 'chicken',
        'icon': '🍗',
        'description': '대한민국 치킨 메뉴 계급도',
        'display_order': 2,
        'display_config': {
            'color': '#FF6B00',
            'heroTitle': '치킨 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 리뷰를 바탕으로 S~B 티어로 분류된 치킨 메뉴 순위표',
            'itemLabel': '메뉴',
            'quizCTA': '나에게 맞는 치킨 찾기',
            'stats': {'modelCount': '30+', 'reviewCount': '1,800+', 'brandCount': '10'},
        },
        'brand_score_definitions': [
            {'key': 'taste', 'label': '맛', 'weight': 35},
            {'key': 'price', 'label': '가성비', 'weight': 25},
            {'key': 'crispy', 'label': '바삭함', 'weight': 20},
            {'key': 'popularity', 'label': '인기도', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'taste', 'label': '맛', 'weight': 35},
            {'key': 'price', 'label': '가성비', 'weight': 25},
            {'key': 'crispy', 'label': '바삭함', 'weight': 20},
            {'key': 'popularity', 'label': '인기도', 'weight': 20},
        ],
        'brands': [
            {'name': '황금올리브치킨', 'slug': 'bbq-golden-olive', 'domain': 'bbq.co.kr', 'brand_name': 'BBQ', 'description': 'BBQ의 시그니처 메뉴, 올리브유로 튀긴 바삭한 치킨', 'scores': {'taste': 96, 'price': 88, 'crispy': 95, 'popularity': 98}},
            {'name': '교촌 오리지날', 'slug': 'kyochon-original', 'domain': 'kyochon.com', 'brand_name': '교촌', 'description': '교촌치킨의 간장 소스 오리지널 치킨', 'scores': {'taste': 95, 'price': 85, 'crispy': 90, 'popularity': 96}},
            {'name': '뿌링클', 'slug': 'bhc-puringkle', 'domain': 'bhc.co.kr', 'brand_name': 'BHC', 'description': 'BHC의 치즈 시즈닝 치킨, MZ세대 인기 1위', 'scores': {'taste': 94, 'price': 85, 'crispy': 92, 'popularity': 97}},
            {'name': '굽네 고추바사삭', 'slug': 'goobne-gochu', 'domain': 'goobne.co.kr', 'brand_name': '굽네', 'description': '오븐에 구운 매콤한 치킨', 'scores': {'taste': 90, 'price': 82, 'crispy': 88, 'popularity': 85}},
            {'name': '네네 스노윙', 'slug': 'nene-snowing', 'domain': 'nenechicken.com', 'brand_name': '네네', 'description': '눈꽃 치즈가 뿌려진 치킨', 'scores': {'taste': 88, 'price': 80, 'crispy': 82, 'popularity': 82}},
            {'name': '푸라닭 블랙알리오', 'slug': 'puradak-black-allio', 'domain': 'puradak.co.kr', 'brand_name': '푸라닭', 'description': '마늘 풍미 가득한 프리미엄 치킨', 'scores': {'taste': 92, 'price': 75, 'crispy': 85, 'popularity': 80}},
            {'name': '맛초킹', 'slug': 'bhc-matchoking', 'domain': 'bhc.co.kr', 'brand_name': 'BHC', 'description': 'BHC의 매콤달콤 양념 치킨', 'scores': {'taste': 86, 'price': 78, 'crispy': 80, 'popularity': 78}},
            {'name': '호식이 후라이드', 'slug': 'hosigi-fried', 'domain': 'hosigi.co.kr', 'brand_name': '호식이', 'description': '가성비 좋은 두마리 치킨', 'scores': {'taste': 78, 'price': 92, 'crispy': 82, 'popularity': 75}},
            {'name': '처갓집 슈프림양념', 'slug': 'cheogajip-supreme', 'domain': 'cheogajip.co.kr', 'brand_name': '처갓집', 'description': '진한 양념의 매력', 'scores': {'taste': 80, 'price': 78, 'crispy': 75, 'popularity': 70}},
            {'name': '60계 후라이드', 'slug': '60gye-fried', 'domain': '60chicken.co.kr', 'brand_name': '60계', 'description': '가성비 치킨의 대명사', 'scores': {'taste': 72, 'price': 95, 'crispy': 78, 'popularity': 72}},
        ],
    },
    {
        'name': '남자시계',
        'slug': 'mens-watch',
        'icon': '⌚',
        'description': '남자 시계 브랜드 계급도 - 커뮤니티 반응 기반',
        'display_order': 3,
        'display_config': {
            'color': '#1E3A5F',
            'heroTitle': '남자시계 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 반응과 브랜드 가치를 바탕으로 S~D 티어로 분류된 시계 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 시계 찾기',
            'stats': {'modelCount': '24', 'reviewCount': '1,200+', 'brandCount': '20'},
        },
        'brand_score_definitions': [
            {'key': 'heritage', 'label': '역사/전통', 'weight': 25},
            {'key': 'craftsmanship', 'label': '기술력', 'weight': 30},
            {'key': 'resale', 'label': '환금성', 'weight': 20},
            {'key': 'prestige', 'label': '브랜드 가치', 'weight': 25},
        ],
        'score_definitions': [
            {'key': 'heritage', 'label': '역사/전통', 'weight': 25},
            {'key': 'craftsmanship', 'label': '기술력', 'weight': 30},
            {'key': 'resale', 'label': '환금성', 'weight': 20},
            {'key': 'prestige', 'label': '브랜드 가치', 'weight': 25},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'dress', 'label': '드레스워치'},
                {'value': 'sport', 'label': '스포츠워치'},
                {'value': 'diver', 'label': '다이버워치'},
                {'value': 'pilot', 'label': '파일럿워치'},
                {'value': 'chronograph', 'label': '크로노그래프'},
            ],
            'usage': [
                {'value': 'formal', 'label': '격식/비즈니스'},
                {'value': 'casual', 'label': '캐주얼'},
                {'value': 'sport', 'label': '스포츠/활동'},
                {'value': 'collection', 'label': '컬렉션/투자'},
            ],
        },
        'brands': [
            # S티어 — 황제
            {'name': '파텍 필립', 'slug': 'patek-philippe', 'domain': 'patek.com', 'description': '시계의 왕, 다음 세대를 위해 보관하는 시계', 'scores': {'heritage': 100, 'craftsmanship': 100, 'resale': 98, 'prestige': 100}},
            {'name': '바쉐론 콘스탄틴', 'slug': 'vacheron-constantin', 'domain': 'vacheron-constantin.com', 'description': '1755년 창립, 세계에서 가장 오래된 시계 매뉴팩처', 'scores': {'heritage': 100, 'craftsmanship': 99, 'resale': 95, 'prestige': 98}},
            {'name': '오데마 피게', 'slug': 'audemars-piguet', 'domain': 'audemarspiguet.com', 'description': '로열 오크의 전설, 럭셔리 스포츠워치의 시작', 'scores': {'heritage': 96, 'craftsmanship': 98, 'resale': 97, 'prestige': 99}},
            {'name': '아 랑에 운트 죄네', 'slug': 'a-lange-soehne', 'domain': 'alange-soehne.com', 'description': '독일 시계 제조의 정수, 완벽한 마감의 대명사', 'scores': {'heritage': 95, 'craftsmanship': 100, 'resale': 93, 'prestige': 97}},
            {'name': '브레게', 'slug': 'breguet', 'domain': 'breguet.com', 'description': '시계 역사의 아버지, 투르비용의 발명자', 'scores': {'heritage': 100, 'craftsmanship': 97, 'resale': 90, 'prestige': 96}},
            # A티어 — 왕
            {'name': '롤렉스', 'slug': 'rolex', 'domain': 'rolex.com', 'description': '시계질의 끝은 결돌롤, 압도적 대중 인지도와 환금성', 'scores': {'heritage': 95, 'craftsmanship': 92, 'resale': 100, 'prestige': 98}},
            {'name': '예거 르쿨트르', 'slug': 'jaeger-lecoultre', 'domain': 'jaeger-lecoultre.com', 'description': '시계 제조사들의 시계 제조사, 1,400개 이상의 칼리버', 'scores': {'heritage': 97, 'craftsmanship': 98, 'resale': 85, 'prestige': 93}},
            {'name': '블랑팡', 'slug': 'blancpain', 'domain': 'blancpain.com', 'description': '1735년 창립, 세계 최초의 시계 브랜드', 'scores': {'heritage': 98, 'craftsmanship': 95, 'resale': 83, 'prestige': 91}},
            {'name': '피아제', 'slug': 'piaget', 'domain': 'piaget.com', 'description': '초박형 무브먼트의 선구자, 주얼리워치의 명가', 'scores': {'heritage': 92, 'craftsmanship': 94, 'resale': 82, 'prestige': 92}},
            # B티어 — 양반
            {'name': '오메가', 'slug': 'omega', 'domain': 'omegawatches.com', 'description': '스피드마스터로 달에 간 시계, 호불호 없는 정답', 'scores': {'heritage': 95, 'craftsmanship': 90, 'resale': 80, 'prestige': 88}},
            {'name': '까르띠에', 'slug': 'cartier', 'domain': 'cartier.com', 'description': '왕의 보석상, 산토스와 탱크의 클래식', 'scores': {'heritage': 96, 'craftsmanship': 85, 'resale': 82, 'prestige': 90}},
            {'name': 'IWC', 'slug': 'iwc', 'domain': 'iwc.com', 'description': '파일럿 워치의 대명사, 엔지니어링의 정수', 'scores': {'heritage': 90, 'craftsmanship': 88, 'resale': 78, 'prestige': 86}},
            {'name': '파네라이', 'slug': 'panerai', 'domain': 'panerai.com', 'description': '이탈리아 해군의 시계, 강렬한 존재감', 'scores': {'heritage': 88, 'craftsmanship': 85, 'resale': 75, 'prestige': 84}},
            {'name': '그랜드 세이코', 'slug': 'grand-seiko', 'domain': 'grand-seiko.com', 'description': '일본 장인 정신의 결정체, 스프링 드라이브의 혁신', 'scores': {'heritage': 85, 'craftsmanship': 92, 'resale': 70, 'prestige': 82}},
            # C티어 — 중인
            {'name': '태그호이어', 'slug': 'tag-heuer', 'domain': 'tagheuer.com', 'description': '사회초년생의 로망, 모터스포츠와 함께한 역사', 'scores': {'heritage': 82, 'craftsmanship': 78, 'resale': 65, 'prestige': 80}},
            {'name': '튜더', 'slug': 'tudor', 'domain': 'tudorwatch.com', 'description': '롤렉스의 동생, 가성비 최고의 럭셔리', 'scores': {'heritage': 78, 'craftsmanship': 80, 'resale': 72, 'prestige': 78}},
            {'name': '론진', 'slug': 'longines', 'domain': 'longines.com', 'description': '190년 역사의 근본, 우아한 클래식 디자인', 'scores': {'heritage': 88, 'craftsmanship': 75, 'resale': 60, 'prestige': 75}},
            {'name': '브라이틀링', 'slug': 'breitling', 'domain': 'breitling.com', 'description': '항공 크로노그래프의 선구자, 나비타이머의 전설', 'scores': {'heritage': 85, 'craftsmanship': 80, 'resale': 62, 'prestige': 76}},
            {'name': '노모스', 'slug': 'nomos', 'domain': 'nomos-glashuette.com', 'description': '독일 바우하우스 디자인, 미니멀한 아름다움', 'scores': {'heritage': 70, 'craftsmanship': 82, 'resale': 58, 'prestige': 72}},
            # D티어 — 평민
            {'name': '티쏘', 'slug': 'tissot', 'domain': 'tissotwatches.com', 'description': 'PRX로 부활, 국밥처럼 든든한 입문용 시계', 'scores': {'heritage': 72, 'craftsmanship': 68, 'resale': 45, 'prestige': 65}},
            {'name': '해밀턴', 'slug': 'hamilton', 'domain': 'hamiltonwatch.com', 'description': '카키필드의 전설, 영화 속 단골 시계', 'scores': {'heritage': 75, 'craftsmanship': 65, 'resale': 42, 'prestige': 62}},
            {'name': '세이코', 'slug': 'seiko', 'domain': 'seikowatches.com', 'description': '쿼츠 혁명의 주역, 가성비 기계식의 대명사', 'scores': {'heritage': 80, 'craftsmanship': 70, 'resale': 40, 'prestige': 58}},
            {'name': '카시오 / 지샥', 'slug': 'casio-gshock', 'domain': 'casio.com', 'description': '진정한 실용성과 내구성의 끝판왕, 툴워치의 정석', 'scores': {'heritage': 65, 'craftsmanship': 72, 'resale': 30, 'prestige': 50}},
            {'name': '애플워치 / 갤럭시워치', 'slug': 'smartwatch', 'domain': 'apple.com', 'description': '일상을 지배한 스마트워치, 기능성의 끝', 'scores': {'heritage': 20, 'craftsmanship': 85, 'resale': 25, 'prestige': 45}},
        ],
    },
]


class Command(BaseCommand):
    help = '카테고리 및 브랜드 시드 데이터 생성'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터 삭제 후 재생성',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('기존 데이터 삭제 중...')
            BrandScore.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()

        for cat_data in CATEGORIES_DATA:
            brands_data = cat_data.pop('brands')

            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            action = '생성' if created else '업데이트'
            self.stdout.write(f'  {cat_data["icon"]} {cat_data["name"]} 카테고리 {action}')

            for brand_data in brands_data:
                scores_data = brand_data.pop('scores')
                domain = brand_data.pop('domain')
                brand_data.pop('brand_name', None)  # 치킨용 brand_name 제거

                brand, b_created = Brand.objects.update_or_create(
                    slug=brand_data['slug'],
                    defaults={
                        'category': category,
                        'name': brand_data['name'],
                        'logo_url': favicon_url(domain),
                        'description': brand_data.get('description', ''),
                    }
                )

                # 동적 점수 생성/업데이트
                for key, value in scores_data.items():
                    label = ''
                    for d in cat_data.get('brand_score_definitions', []):
                        if d['key'] == key:
                            label = d['label']
                            break

                    BrandScore.objects.update_or_create(
                        brand=brand,
                        key=key,
                        defaults={'value': value, 'label': label}
                    )

                b_action = '생성' if b_created else '업데이트'
                self.stdout.write(f'    {brand.tier}티어 {brand.name} {b_action} (점수: {brand.tier_score:.1f})')

            # pop한 brands를 다시 넣어줌 (재실행 대비)
            cat_data['brands'] = brands_data

        self.stdout.write(self.style.SUCCESS('\n시드 데이터 생성 완료!'))
        self.stdout.write(f'  카테고리: {Category.objects.count()}개')
        self.stdout.write(f'  브랜드: {Brand.objects.count()}개')
        self.stdout.write(f'  브랜드 점수: {BrandScore.objects.count()}개')
