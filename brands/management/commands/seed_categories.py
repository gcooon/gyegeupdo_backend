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
        'group': 'sports',
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
        'group': 'food',
        'description': '대한민국 치킨 프랜차이즈 계급도',
        'display_order': 2,
        'display_config': {
            'color': '#FF6B00',
            'heroTitle': '치킨 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 리뷰를 바탕으로 S~B 티어로 분류된 치킨 프랜차이즈 순위표',
            'itemLabel': '프랜차이즈',
            'quizCTA': '나에게 맞는 치킨 찾기',
            'stats': {'modelCount': '30+', 'reviewCount': '1,800+', 'brandCount': '10'},
        },
        'brand_score_definitions': [
            {'key': 'taste', 'label': '맛 평균', 'weight': 35},
            {'key': 'price', 'label': '가성비', 'weight': 25},
            {'key': 'variety', 'label': '메뉴 다양성', 'weight': 20},
            {'key': 'accessibility', 'label': '접근성', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'taste', 'label': '맛', 'weight': 35},
            {'key': 'price', 'label': '가성비', 'weight': 25},
            {'key': 'crispy', 'label': '바삭함', 'weight': 20},
            {'key': 'popularity', 'label': '인기도', 'weight': 20},
        ],
        'spec_definitions': [
            {'key': 'price', 'label': '가격', 'unit': '원', 'type': 'number'},
            {'key': 'calories', 'label': '칼로리', 'unit': 'kcal', 'type': 'number'},
            {'key': 'serving', 'label': '제공량', 'unit': 'g', 'type': 'number'},
            {'key': 'spicy_level', 'label': '맵기', 'type': 'text'},
            {'key': 'cooking_method', 'label': '조리방식', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'fried', 'label': '후라이드'},
                {'value': 'seasoned', 'label': '양념'},
                {'value': 'soy', 'label': '간장'},
                {'value': 'cheese', 'label': '치즈'},
                {'value': 'garlic', 'label': '마늘'},
                {'value': 'roasted', 'label': '구이'},
            ],
            'usage': [
                {'value': 'solo', 'label': '혼닭'},
                {'value': 'party', 'label': '파티'},
                {'value': 'beer', 'label': '치맥'},
                {'value': 'family', 'label': '가족'},
            ],
        },
        'brands': [
            # S티어 — 황제 (프랜차이즈)
            {'name': 'BBQ', 'slug': 'bbq', 'domain': 'bbq.co.kr', 'description': '황금올리브치킨의 BBQ, 올리브유 치킨의 원조', 'scores': {'taste': 95, 'price': 82, 'variety': 92, 'accessibility': 95}},
            {'name': 'BHC', 'slug': 'bhc', 'domain': 'bhc.co.kr', 'description': '뿌링클, 맛초킹의 BHC, MZ세대 인기 1위', 'scores': {'taste': 93, 'price': 80, 'variety': 95, 'accessibility': 92}},
            {'name': '교촌치킨', 'slug': 'kyochon', 'domain': 'kyochon.com', 'description': '간장 치킨의 명가, 프리미엄 치킨의 대명사', 'scores': {'taste': 94, 'price': 78, 'variety': 88, 'accessibility': 90}},
            # A티어 — 왕
            {'name': '굽네치킨', 'slug': 'goobne', 'domain': 'goobne.co.kr', 'description': '오븐구이 치킨의 선두주자, 건강한 치킨', 'scores': {'taste': 88, 'price': 80, 'variety': 85, 'accessibility': 88}},
            {'name': '네네치킨', 'slug': 'nene', 'domain': 'nenechicken.com', 'description': '스노윙 치킨의 네네, 다양한 시즈닝', 'scores': {'taste': 85, 'price': 82, 'variety': 90, 'accessibility': 85}},
            {'name': '푸라닭', 'slug': 'puradak', 'domain': 'puradak.co.kr', 'description': '블랙알리오의 푸라닭, 프리미엄 마늘 치킨', 'scores': {'taste': 90, 'price': 72, 'variety': 78, 'accessibility': 80}},
            # B티어 — 양반
            {'name': '호식이두마리치킨', 'slug': 'hosigi', 'domain': 'hosigi.co.kr', 'description': '두마리 치킨의 원조, 가성비 최강', 'scores': {'taste': 78, 'price': 95, 'variety': 75, 'accessibility': 82}},
            {'name': '처갓집양념치킨', 'slug': 'cheogajip', 'domain': 'cheogajip.co.kr', 'description': '전통 양념 치킨의 명가', 'scores': {'taste': 82, 'price': 78, 'variety': 72, 'accessibility': 78}},
            {'name': '60계치킨', 'slug': '60gye', 'domain': '60chicken.co.kr', 'description': '6천원대 치킨의 시작, 가성비 치킨', 'scores': {'taste': 75, 'price': 98, 'variety': 70, 'accessibility': 85}},
            {'name': 'KFC', 'slug': 'kfc', 'domain': 'kfc.co.kr', 'description': '오리지널 레시피의 KFC, 글로벌 치킨 브랜드', 'scores': {'taste': 80, 'price': 70, 'variety': 80, 'accessibility': 92}},
        ],
    },
    {
        'name': '남자시계',
        'slug': 'mens-watch',
        'icon': '⌚',
        'group': 'tech',
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
        'spec_definitions': [
            {'key': 'case_diameter', 'label': '케이스 직경', 'unit': 'mm', 'type': 'number'},
            {'key': 'case_thickness', 'label': '케이스 두께', 'unit': 'mm', 'type': 'number'},
            {'key': 'water_resistance', 'label': '방수', 'unit': 'm', 'type': 'number'},
            {'key': 'movement', 'label': '무브먼트', 'type': 'text'},
            {'key': 'power_reserve', 'label': '파워리저브', 'unit': '시간', 'type': 'number'},
            {'key': 'case_material', 'label': '케이스 소재', 'type': 'text'},
            {'key': 'crystal', 'label': '글라스', 'type': 'text'},
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
    {
        'name': '뜨는 패션 브랜드',
        'slug': 'fashion-brands',
        'icon': '👗',
        'group': 'lifestyle',
        'description': '뜨는 패션 브랜드 계급도 - 커뮤니티 인정 + 현재 하이프 기반',
        'display_order': 4,
        'display_config': {
            'color': '#8B5CF6',
            'heroTitle': '뜨는 패션 브랜드 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 계급도와 Lyst Index를 결합해 S~D 티어로 분류된 패션 브랜드 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 패션 브랜드 찾기',
            'stats': {'modelCount': '50+', 'reviewCount': '1,000+', 'brandCount': '33'},
        },
        'brand_score_definitions': [
            {'key': 'trend', 'label': '트렌드/화제성', 'weight': 35},
            {'key': 'design', 'label': '디자인 혁신성', 'weight': 25},
            {'key': 'community', 'label': '커뮤니티 인정도', 'weight': 25},
            {'key': 'value', 'label': '가치/희소성', 'weight': 15},
        ],
        'score_definitions': [
            {'key': 'design', 'label': '디자인', 'weight': 30},
            {'key': 'quality', 'label': '품질', 'weight': 25},
            {'key': 'trend', 'label': '트렌드 반영', 'weight': 25},
            {'key': 'value', 'label': '가격 대비 가치', 'weight': 20},
        ],
        'spec_definitions': [
            {'key': 'price_range', 'label': '가격대', 'type': 'text'},
            {'key': 'country', 'label': '원산지', 'type': 'text'},
            {'key': 'founded_year', 'label': '설립연도', 'unit': '년', 'type': 'number'},
            {'key': 'brand_category', 'label': '브랜드 성격', 'type': 'select', 'options': [
                {'value': 'luxury', 'label': '럭셔리'},
                {'value': 'street', 'label': '스트릿'},
                {'value': 'contemporary', 'label': '컨템포러리'},
                {'value': 'outdoor', 'label': '아웃도어'},
                {'value': 'korean', 'label': '국내신진'},
            ]},
            {'key': 'key_item', 'label': '대표 아이템', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'bag', 'label': '가방'},
                {'value': 'outerwear', 'label': '아우터'},
                {'value': 'knitwear', 'label': '니트웨어'},
                {'value': 'shoes', 'label': '신발'},
                {'value': 'accessory', 'label': '액세서리'},
            ],
            'usage': [
                {'value': 'formal', 'label': '격식/포멀'},
                {'value': 'casual', 'label': '캐주얼'},
                {'value': 'street', 'label': '스트릿'},
                {'value': 'outdoor', 'label': '아웃도어'},
            ],
        },
        'brands': [
            # S티어 — 황제: 커뮤니티 Tier 0-1A + 현재 하이프 유지
            {'name': '에르메스', 'slug': 'hermes', 'domain': 'hermes.com', 'description': '모든 커뮤니티 계급도 Tier 0 고정, 버킨백 대기 리스트가 곧 브랜드 파워의 증거', 'scores': {'trend': 95, 'design': 92, 'community': 98, 'value': 100}},
            {'name': '샤넬', 'slug': 'chanel', 'domain': 'chanel.com', 'description': '매년 가격 인상에도 수요 불변, 커뮤니티 3대 명품 고정석', 'scores': {'trend': 88, 'design': 88, 'community': 95, 'value': 95}},
            {'name': '미우미우', 'slug': 'miu-miu', 'domain': 'miumiu.com', 'description': 'Lyst Index 연속 1위, MZ세대 워너비 럭셔리의 정점', 'scores': {'trend': 98, 'design': 95, 'community': 92, 'value': 80}},
            {'name': '로에베', 'slug': 'loewe', 'domain': 'loewe.com', 'description': '조나단 앤더슨의 크래프트 럭셔리, Lyst Index 상위권 고정', 'scores': {'trend': 97, 'design': 96, 'community': 90, 'value': 82}},
            {'name': '더 로우', 'slug': 'the-row', 'domain': 'therow.com', 'description': '콰이어트 럭셔리 트렌드의 교과서, 로고 없이 소재로 승부', 'scores': {'trend': 92, 'design': 90, 'community': 88, 'value': 85}},
            {'name': '브루넬로 쿠치넬리', 'slug': 'brunello-cucinelli', 'domain': 'brunellocucinelli.com', 'description': '캐시미어의 왕, 실리콘밸리 CEO 유니폼 + 주가 5배 상승', 'scores': {'trend': 85, 'design': 82, 'community': 88, 'value': 92}},
            # A티어 — 왕: 커뮤니티 Tier 1B-2 + Lyst Index 상위권
            {'name': '보테가 베네타', 'slug': 'bottega-veneta', 'domain': 'bottegaveneta.com', 'description': '인트레치아토 위빙의 로고 없는 럭셔리, Lyst 상위권 유지', 'scores': {'trend': 82, 'design': 88, 'community': 82, 'value': 78}},
            {'name': '프라다', 'slug': 'prada', 'domain': 'prada.com', 'description': '라프 시몬스 합류 후 힙한 명품으로 부상, 리나일론 대히트', 'scores': {'trend': 85, 'design': 82, 'community': 78, 'value': 80}},
            {'name': '아크테릭스', 'slug': 'arcteryx', 'domain': 'arcteryx.com', 'description': '고프코어 절대 왕자, 아웃도어계의 에르메스로 불림', 'scores': {'trend': 90, 'design': 80, 'community': 85, 'value': 65}},
            {'name': '디올', 'slug': 'dior-fashion', 'domain': 'dior.com', 'description': '커뮤니티 Tier 1B 고정, 셀럽 앰배서더 효과로 안정적 인기', 'scores': {'trend': 78, 'design': 80, 'community': 82, 'value': 85}},
            {'name': '생 로랑', 'slug': 'saint-laurent', 'domain': 'ysl.com', 'description': '가장 쿨한 프렌치 럭셔리, 록시크 무드의 대표', 'scores': {'trend': 75, 'design': 82, 'community': 80, 'value': 82}},
            {'name': '셀린느', 'slug': 'celine', 'domain': 'celine.com', 'description': '피비 파일로 레거시 + 트리옹프 라인 꾸준한 인기', 'scores': {'trend': 76, 'design': 84, 'community': 78, 'value': 78}},
            # B티어 — 양반: 컨템포러리/패션피플 인정 브랜드
            {'name': '에메 레온 도레', 'slug': 'aime-leon-dore', 'domain': 'aimeleondore.com', 'description': '뉴발란스 콜라보 대히트, 프렙+스트릿 믹스의 정석', 'scores': {'trend': 80, 'design': 82, 'community': 72, 'value': 45}},
            {'name': '스톤 아일랜드', 'slug': 'stone-island', 'domain': 'stoneisland.com', 'description': '와펜 패치의 테크니컬 캐주얼, 유럽 축구 문화와 결합된 컬트', 'scores': {'trend': 72, 'design': 75, 'community': 78, 'value': 62}},
            {'name': '메종 마르지엘라', 'slug': 'maison-margiela', 'domain': 'maisonmargiela.com', 'description': '타비 부츠 = 패션피플 시그널, 해체주의 럭셔리의 대명사', 'scores': {'trend': 68, 'design': 90, 'community': 65, 'value': 58}},
            {'name': '아크네 스튜디오', 'slug': 'acne-studios', 'domain': 'acnestudios.com', 'description': '페이스 패치 머플러의 스칸디 미니멀, 입문 럭셔리 컨템포러리', 'scores': {'trend': 70, 'design': 80, 'community': 68, 'value': 55}},
            {'name': '아워 레거시', 'slug': 'our-legacy', 'domain': 'ourlegacy.com', 'description': 'Reddit MFA 추천 1위 컨템포러리, 워크웨어+테일러링 혼합', 'scores': {'trend': 72, 'design': 78, 'community': 65, 'value': 48}},
            {'name': '스포티 앤 리치', 'slug': 'sporty-and-rich', 'domain': 'sportyandrich.com', 'description': '올드머니+웰니스 트렌드 정조준, 인스타 감성 브랜드', 'scores': {'trend': 75, 'design': 72, 'community': 68, 'value': 40}},
            {'name': '코스', 'slug': 'cos', 'domain': 'cos.com', 'description': '10만원대 미니멀 럭셔리 감성, 커뮤니티 입문 추천 1순위', 'scores': {'trend': 68, 'design': 72, 'community': 70, 'value': 45}},
            # C티어 — 중인: 얼리어답터/패션위크 주목, 대중 인지도 제한적
            {'name': '보데', 'slug': 'bode', 'domain': 'bodenewyork.com', 'description': 'CFDA 수상 남성복 혁명, 빈티지 원단의 크래프트 디자인', 'scores': {'trend': 60, 'design': 82, 'community': 48, 'value': 35}},
            {'name': '르메르', 'slug': 'lemaire', 'domain': 'lemaire.fr', 'description': '유니클로 U 콜라보로 대중화, 합리적 프렌치 미니멀', 'scores': {'trend': 62, 'design': 75, 'community': 52, 'value': 42}},
            {'name': '웨일즈 보너', 'slug': 'wales-bonner', 'domain': 'walesbonner.net', 'description': '아디다스 삼바 콜라보 리셀 폭등, LVMH Prize 수상', 'scores': {'trend': 68, 'design': 78, 'community': 45, 'value': 32}},
            {'name': '로에 (Róhe)', 'slug': 'rohe', 'domain': 'rohe.com', 'description': '에포트리스 유러피안 미학, 패션 에디터 픽 신성', 'scores': {'trend': 62, 'design': 75, 'community': 42, 'value': 30}},
            {'name': '키코 코스타디노프', 'slug': 'kiko-kostadinov', 'domain': 'kikokostadinov.com', 'description': '아식스 콜라보 스니커즈 컬렉터 필수, 아방가르드 디자인', 'scores': {'trend': 58, 'design': 80, 'community': 40, 'value': 28}},
            {'name': '앤더슨벨', 'slug': 'andersson-bell', 'domain': 'anderssonbell.com', 'description': '파리 패션위크 진출 K-패션 대표, 해외 셀렉트숍 입점', 'scores': {'trend': 60, 'design': 68, 'community': 50, 'value': 30}},
            {'name': '우영미', 'slug': 'wooyoungmi', 'domain': 'wooyoungmi.com', 'description': '파리 남성 패션위크 정규 쇼 20년+, 해외 먼저 인정받은 K-디자이너', 'scores': {'trend': 52, 'design': 70, 'community': 45, 'value': 38}},
            {'name': '자크뮈스', 'slug': 'jacquemus', 'domain': 'jacquemus.com', 'description': '미니백 트렌드 시작점이었으나 최근 하이프 안정화', 'scores': {'trend': 55, 'design': 72, 'community': 48, 'value': 32}},
            # D티어 — 평민: 인지도는 있으나 하이프 하락/대중화로 희소성 저하
            {'name': '오프화이트', 'slug': 'off-white', 'domain': 'off---white.com', 'description': '버질 사후 방향성 상실, 커뮤니티 한물간 하이프 평가', 'scores': {'trend': 30, 'design': 60, 'community': 38, 'value': 25}},
            {'name': '구찌', 'slug': 'gucci-fashion', 'domain': 'gucci.com', 'description': '사바토 데 사르노 전환 후 매출 하락세, 하이프 냉각', 'scores': {'trend': 35, 'design': 55, 'community': 42, 'value': 50}},
            {'name': '발렌시아가', 'slug': 'balenciaga', 'domain': 'balenciaga.com', 'description': '광고 논란 + 하이프 피로감, 논란의 브랜드 꼬리표', 'scores': {'trend': 32, 'design': 58, 'community': 35, 'value': 40}},
            {'name': '피어 오브 갓', 'slug': 'fear-of-god', 'domain': 'fearofgod.com', 'description': 'Essentials 대중화가 브랜드 가치 희석, 에센셜즈 피로감', 'scores': {'trend': 30, 'design': 55, 'community': 35, 'value': 22}},
            {'name': '톰 브라운', 'slug': 'thom-browne', 'domain': 'thombrowne.com', 'description': '디자인은 인정하지만 좁은 팬덤에 갇힌 브랜드', 'scores': {'trend': 28, 'design': 72, 'community': 38, 'value': 35}},
            {'name': '베트멍', 'slug': 'vetements', 'domain': 'vetementswebsite.com', 'description': '뎀나 퇴장 후 하이프 소멸, 2017년 브랜드 평가 고착', 'scores': {'trend': 18, 'design': 50, 'community': 25, 'value': 20}},
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
