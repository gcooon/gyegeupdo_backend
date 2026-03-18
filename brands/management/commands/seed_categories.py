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
    {
        'name': '카메라',
        'slug': 'camera',
        'icon': '📷',
        'group': 'tech',
        'description': '카메라 브랜드 계급도 - 2024~2026 미러리스 시대 기준',
        'display_order': 5,
        'display_config': {
            'color': '#1A1A2E',
            'heroTitle': '카메라 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 반응과 전문 리뷰를 바탕으로 S~D 티어로 분류된 카메라 브랜드 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 카메라 찾기',
            'stats': {'modelCount': '55+', 'reviewCount': '3,000+', 'brandCount': '15'},
        },
        'brand_score_definitions': [
            {'key': 'image_quality', 'label': '화질', 'weight': 30},
            {'key': 'af_performance', 'label': 'AF 성능', 'weight': 25},
            {'key': 'build_quality', 'label': '빌드 퀄리티', 'weight': 20},
            {'key': 'ecosystem', 'label': '생태계', 'weight': 25},
        ],
        'score_definitions': [
            {'key': 'image_quality', 'label': '화질', 'weight': 30},
            {'key': 'af_performance', 'label': 'AF 성능', 'weight': 25},
            {'key': 'build_quality', 'label': '빌드 퀄리티', 'weight': 20},
            {'key': 'value', 'label': '가성비', 'weight': 25},
        ],
        'spec_definitions': [
            {'key': 'sensor_size', 'label': '센서 크기', 'type': 'text'},
            {'key': 'megapixels', 'label': '유효 화소', 'unit': 'MP', 'type': 'number'},
            {'key': 'weight', 'label': '무게 (바디)', 'unit': 'g', 'type': 'number'},
            {'key': 'max_fps', 'label': '최대 연사', 'unit': 'fps', 'type': 'number'},
            {'key': 'video_resolution', 'label': '최대 동영상', 'type': 'text'},
            {'key': 'viewfinder', 'label': '뷰파인더', 'type': 'text'},
            {'key': 'stabilization', 'label': '손떨림 보정', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'mirrorless', 'label': '미러리스'},
                {'value': 'dslr', 'label': 'DSLR'},
                {'value': 'compact', 'label': '컴팩트'},
                {'value': 'action', 'label': '액션캠'},
                {'value': 'medium_format', 'label': '중형포맷'},
                {'value': 'instant', 'label': '인스턴트'},
            ],
            'usage': [
                {'value': 'professional', 'label': '프로/보도'},
                {'value': 'enthusiast', 'label': '하이아마추어'},
                {'value': 'travel', 'label': '여행/일상'},
                {'value': 'vlog', 'label': '브이로그/영상'},
                {'value': 'landscape', 'label': '풍경/건축'},
                {'value': 'sports', 'label': '스포츠/야생'},
            ],
        },
        'brands': [
            # S티어 — 황제: 빅3, 미러리스 시대 최상위
            {'name': '캐논', 'slug': 'canon', 'domain': 'canon.com', 'description': 'RF 마운트로 미러리스 시대를 재편한 카메라의 왕. EOS R 시스템과 압도적 렌즈 라인업', 'scores': {'image_quality': 92, 'af_performance': 95, 'build_quality': 90, 'ecosystem': 98}},
            {'name': '소니', 'slug': 'sony', 'domain': 'sony.com', 'description': '미러리스 혁명의 선두주자. A7/A9 시리즈와 최고 수준의 AF·센서 기술력', 'scores': {'image_quality': 95, 'af_performance': 97, 'build_quality': 88, 'ecosystem': 95}},
            {'name': '니콘', 'slug': 'nikon', 'domain': 'nikon.com', 'description': 'Z 마운트로 부활한 니콘. Z8/Z9으로 프로 시장 재진입, 최고 수준의 센서 화질', 'scores': {'image_quality': 96, 'af_performance': 93, 'build_quality': 92, 'ecosystem': 90}},
            # A티어 — 왕: 특화 영역에서 강자
            {'name': '후지필름', 'slug': 'fujifilm', 'domain': 'fujifilm.com', 'description': 'APS-C와 중형포맷의 양대 라인업. 필름 시뮬레이션과 레트로 디자인의 대명사', 'scores': {'image_quality': 90, 'af_performance': 82, 'build_quality': 85, 'ecosystem': 82}},
            {'name': '파나소닉', 'slug': 'panasonic-lumix', 'domain': 'panasonic.com', 'description': 'S5 II부터 위상차 AF 탑재. 동영상 성능 최강, 루믹스 S 풀프레임 시스템', 'scores': {'image_quality': 88, 'af_performance': 80, 'build_quality': 82, 'ecosystem': 75}},
            {'name': '라이카', 'slug': 'leica', 'domain': 'leica-camera.com', 'description': '카메라의 에르메스. M 시스템과 Q 시리즈의 전설적 광학, 사진 문화의 아이콘', 'scores': {'image_quality': 92, 'af_performance': 68, 'build_quality': 98, 'ecosystem': 62}},
            {'name': 'OM System', 'slug': 'om-system', 'domain': 'om-system.com', 'description': '구 올림푸스. 마이크로 포서드의 강자, 초소형·초경량·방진방적의 아웃도어 특화', 'scores': {'image_quality': 78, 'af_performance': 80, 'build_quality': 88, 'ecosystem': 75}},
            # B티어 — 양반: 니치 영역 강자
            {'name': '리코/펜탁스', 'slug': 'ricoh-pentax', 'domain': 'ricoh-imaging.com', 'description': 'GR III 시리즈의 스트릿 포토 아이콘 + 펜탁스 DSLR 마니아층. OVF를 고수하는 장인정신', 'scores': {'image_quality': 82, 'af_performance': 60, 'build_quality': 82, 'ecosystem': 55}},
            {'name': '시그마', 'slug': 'sigma', 'domain': 'sigma-global.com', 'description': 'fp 시리즈의 초소형 풀프레임. Art/Contemporary 렌즈 라인업은 업계 최고 수준', 'scores': {'image_quality': 85, 'af_performance': 65, 'build_quality': 75, 'ecosystem': 60}},
            {'name': '핫셀블라드', 'slug': 'hasselblad', 'domain': 'hasselblad.com', 'description': '중형포맷의 전설. X2D 100C로 디지털 중형 시대를 선도, 1억 화소의 압도적 화질', 'scores': {'image_quality': 98, 'af_performance': 62, 'build_quality': 92, 'ecosystem': 45}},
            {'name': 'DJI', 'slug': 'dji', 'domain': 'dji.com', 'description': '드론 1위 DJI의 카메라 진출. Osmo Action 시리즈와 짐벌 카메라의 강자', 'scores': {'image_quality': 68, 'af_performance': 72, 'build_quality': 78, 'ecosystem': 65}},
            # C티어 — 중인: 특수 분야 특화
            {'name': '고프로', 'slug': 'gopro', 'domain': 'gopro.com', 'description': '액션캠의 원조. Hero 시리즈로 익스트림 스포츠 촬영의 대명사', 'scores': {'image_quality': 58, 'af_performance': 55, 'build_quality': 80, 'ecosystem': 62}},
            {'name': 'Insta360', 'slug': 'insta360', 'domain': 'insta360.com', 'description': '360도 카메라와 AI 편집의 혁신자. X4와 Ace Pro로 액션캠 시장 도전', 'scores': {'image_quality': 55, 'af_performance': 50, 'build_quality': 72, 'ecosystem': 58}},
            # D티어 — 평민: 시장 영향력 약화
            {'name': '캐논 (보급)', 'slug': 'canon-budget', 'domain': 'canon.com', 'description': 'EOS M 단종 후 R100으로 보급 시장 유지. 기능 제한이 아쉬운 엔트리 라인업', 'scores': {'image_quality': 65, 'af_performance': 55, 'build_quality': 50, 'ecosystem': 45}},
            {'name': '코닥', 'slug': 'kodak', 'domain': 'kodak.com', 'description': '필름의 전설이었던 코닥. 현재는 인스턴트/토이 카메라 위주로 명맥 유지', 'scores': {'image_quality': 30, 'af_performance': 20, 'build_quality': 35, 'ecosystem': 20}},
        ],
    },
    # ============================================================
    # 자동차 브랜드 계급도
    # ============================================================
    {
        'name': '자동차',
        'slug': 'car-brands',
        'icon': '🚗',
        'group': 'lifestyle',
        'description': '자동차 브랜드 계급도 - 커뮤니티 평판과 전문 리뷰 기반',
        'display_order': 6,
        'display_config': {
            'color': '#0F172A',
            'heroTitle': '자동차 브랜드 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 평판과 전문 리뷰를 바탕으로 S~D 티어로 분류된 자동차 브랜드 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 차 찾기',
            'stats': {'modelCount': '50+', 'reviewCount': '5,000+', 'brandCount': '20'},
        },
        'brand_score_definitions': [
            {'key': 'performance', 'label': '성능', 'weight': 25},
            {'key': 'reliability', 'label': '신뢰성', 'weight': 30},
            {'key': 'brand_value', 'label': '브랜드 가치', 'weight': 20},
            {'key': 'value_for_money', 'label': '가성비', 'weight': 25},
        ],
        'score_definitions': [
            {'key': 'performance', 'label': '성능', 'weight': 25},
            {'key': 'comfort', 'label': '편의성', 'weight': 25},
            {'key': 'reliability', 'label': '신뢰성', 'weight': 25},
            {'key': 'value', 'label': '가성비', 'weight': 25},
        ],
        'spec_definitions': [
            {'key': 'engine', 'label': '엔진/파워트레인', 'type': 'text'},
            {'key': 'horsepower', 'label': '최대출력', 'unit': 'hp', 'type': 'number'},
            {'key': 'fuel_economy', 'label': '연비', 'unit': 'km/L', 'type': 'number'},
            {'key': 'price', 'label': '시작가', 'unit': '만원', 'type': 'number'},
            {'key': 'size', 'label': '차급', 'type': 'text'},
            {'key': 'drive', 'label': '구동방식', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'sedan', 'label': '세단'},
                {'value': 'suv', 'label': 'SUV'},
                {'value': 'ev', 'label': '전기차'},
                {'value': 'sports', 'label': '스포츠카'},
                {'value': 'truck', 'label': '트럭/픽업'},
            ],
            'usage': [
                {'value': 'commute', 'label': '출퇴근'},
                {'value': 'family', 'label': '패밀리'},
                {'value': 'luxury', 'label': '럭셔리'},
                {'value': 'performance', 'label': '퍼포먼스'},
                {'value': 'outdoor', 'label': '아웃도어'},
            ],
        },
        'brands': [
            # S티어 — 황제
            {'name': '메르세데스-벤츠', 'slug': 'mercedes-benz', 'domain': 'mercedes-benz.com', 'description': '자동차의 발명자. S클래스로 대표되는 럭셔리의 정점, AMG 퍼포먼스와 EQ 전동화까지', 'scores': {'performance': 92, 'reliability': 82, 'brand_value': 98, 'value_for_money': 60}},
            {'name': 'BMW', 'slug': 'bmw', 'domain': 'bmw.com', 'description': '주행의 즐거움(Freude am Fahren). M 시리즈의 퍼포먼스와 iX의 전동화 리더십', 'scores': {'performance': 95, 'reliability': 80, 'brand_value': 95, 'value_for_money': 62}},
            {'name': '포르쉐', 'slug': 'porsche', 'domain': 'porsche.com', 'description': '911의 전설. 스포츠카와 SUV 모두에서 최고의 드라이빙을 제공하는 브랜드', 'scores': {'performance': 98, 'reliability': 88, 'brand_value': 97, 'value_for_money': 55}},
            # A티어 — 왕
            {'name': '아우디', 'slug': 'audi', 'domain': 'audi.com', 'description': '기술을 통한 진보(Vorsprung durch Technik). 콰트로 AWD와 세련된 인테리어의 대명사', 'scores': {'performance': 88, 'reliability': 78, 'brand_value': 88, 'value_for_money': 65}},
            {'name': '렉서스', 'slug': 'lexus', 'domain': 'lexus.com', 'description': '토요타의 럭셔리. 압도적 신뢰성과 정숙성, 하이브리드 기술의 선두주자', 'scores': {'performance': 78, 'reliability': 96, 'brand_value': 82, 'value_for_money': 75}},
            {'name': '볼보', 'slug': 'volvo', 'domain': 'volvocars.com', 'description': '안전의 대명사. 북유럽 미니멀 디자인과 업계 최고 수준의 안전 기술', 'scores': {'performance': 80, 'reliability': 85, 'brand_value': 80, 'value_for_money': 72}},
            {'name': '테슬라', 'slug': 'tesla', 'domain': 'tesla.com', 'description': '전기차 혁명의 선두주자. 오토파일럿과 OTA 업데이트로 자동차 산업을 재정의', 'scores': {'performance': 90, 'reliability': 68, 'brand_value': 90, 'value_for_money': 75}},
            # B티어 — 양반
            {'name': '토요타', 'slug': 'toyota', 'domain': 'toyota.com', 'description': '세계 판매 1위. 캠리/RAV4의 대중성과 랜드크루저의 내구성, 하이브리드의 원조', 'scores': {'performance': 72, 'reliability': 95, 'brand_value': 78, 'value_for_money': 85}},
            {'name': '혼다', 'slug': 'honda', 'domain': 'honda.com', 'description': '엔진의 혼다. 시빅/어코드의 탄탄한 라인업과 VTEC 기술력, 탁월한 잔고장 없음', 'scores': {'performance': 75, 'reliability': 92, 'brand_value': 72, 'value_for_money': 85}},
            {'name': '제네시스', 'slug': 'genesis', 'domain': 'genesis.com', 'description': '현대차의 럭셔리. G80/GV70으로 독일 3사에 도전하는 한국 프리미엄 브랜드', 'scores': {'performance': 82, 'reliability': 80, 'brand_value': 70, 'value_for_money': 82}},
            {'name': '폭스바겐', 'slug': 'volkswagen', 'domain': 'volkswagen.com', 'description': '국민차의 원조. 골프/티구안의 대중성과 ID 시리즈의 전동화, 탄탄한 기본기', 'scores': {'performance': 78, 'reliability': 72, 'brand_value': 75, 'value_for_money': 70}},
            {'name': '마쯔다', 'slug': 'mazda', 'domain': 'mazda.com', 'description': '인마일체(人馬一体). MX-5 미아타로 대표되는 드라이빙의 즐거움, 스카이액티브 기술', 'scores': {'performance': 80, 'reliability': 85, 'brand_value': 65, 'value_for_money': 78}},
            # C티어 — 중인
            {'name': '현대', 'slug': 'hyundai', 'domain': 'hyundai.com', 'description': '한국 자동차의 대표. 아이오닉/투싼의 글로벌 인기와 빠른 전동화 전환', 'scores': {'performance': 72, 'reliability': 75, 'brand_value': 65, 'value_for_money': 88}},
            {'name': '기아', 'slug': 'kia', 'domain': 'kia.com', 'description': '디자인 혁신의 기아. EV6/EV9과 K시리즈의 가성비, 피터 슈라이어 디자인 유산', 'scores': {'performance': 72, 'reliability': 74, 'brand_value': 62, 'value_for_money': 90}},
            {'name': '닛산', 'slug': 'nissan', 'domain': 'nissan.com', 'description': 'GT-R의 전설과 리프의 전기차 선구자. 최근 라인업 노후화가 아쉬운 브랜드', 'scores': {'performance': 70, 'reliability': 72, 'brand_value': 60, 'value_for_money': 75}},
            {'name': '쉐보레', 'slug': 'chevrolet', 'domain': 'chevrolet.com', 'description': '아메리칸 머슬의 상징. 카마로/콜벳의 퍼포먼스와 트래버스/이쿼녹스의 대중성', 'scores': {'performance': 75, 'reliability': 68, 'brand_value': 65, 'value_for_money': 78}},
            # D티어 — 평민
            {'name': '스즈키', 'slug': 'suzuki', 'domain': 'suzuki.com', 'description': '소형차/경차 전문. 짐니의 매니아층이 있지만 한국 시장에서는 철수', 'scores': {'performance': 55, 'reliability': 78, 'brand_value': 40, 'value_for_money': 80}},
            {'name': '미쓰비시', 'slug': 'mitsubishi', 'domain': 'mitsubishi-motors.com', 'description': 'EVO의 영광은 과거. 현재는 아웃랜더 중심의 제한적 라인업으로 시장 영향력 감소', 'scores': {'performance': 55, 'reliability': 65, 'brand_value': 42, 'value_for_money': 72}},
            {'name': '르노', 'slug': 'renault', 'domain': 'renault.com', 'description': '유럽 대중차의 대표였으나 한국에서는 르노코리아로 존재감 약화. SM6/XM3 중심', 'scores': {'performance': 60, 'reliability': 58, 'brand_value': 45, 'value_for_money': 68}},
            # S티어 추가 — 슈퍼카/초럭셔리
            {'name': '페라리', 'slug': 'ferrari', 'domain': 'ferrari.com', 'description': '프랜싱 호스의 전설. F1 DNA를 가진 최고의 스포츠카 메이커', 'scores': {'performance': 99, 'reliability': 80, 'brand_value': 99, 'value_for_money': 35}},
            {'name': '람보르기니', 'slug': 'lamborghini', 'domain': 'lamborghini.com', 'description': '아벤타도르와 우라칸의 황소. 가장 공격적이고 화려한 슈퍼카 브랜드', 'scores': {'performance': 97, 'reliability': 75, 'brand_value': 97, 'value_for_money': 30}},
            {'name': '맥라렌', 'slug': 'mclaren', 'domain': 'mclaren.com', 'description': 'F1 기술의 민간 이전. 720S와 Artura로 대표되는 퓨어 스포츠카 전문', 'scores': {'performance': 98, 'reliability': 72, 'brand_value': 92, 'value_for_money': 32}},
            {'name': '벤틀리', 'slug': 'bentley', 'domain': 'bentleymotor.com', 'description': '궁극의 그랜드 투어러. 컨티넨탈 GT와 벤테이가의 초럭셔리 세계', 'scores': {'performance': 88, 'reliability': 82, 'brand_value': 95, 'value_for_money': 38}},
            {'name': '롤스로이스', 'slug': 'rolls-royce', 'domain': 'rolls-roycemotorcars.com', 'description': '자동차 럭셔리의 절대 정점. 팬텀과 고스트, 움직이는 궁전', 'scores': {'performance': 82, 'reliability': 85, 'brand_value': 99, 'value_for_money': 25}},
            # A티어 추가 — GT/럭셔리 SUV
            {'name': '에스턴 마틴', 'slug': 'aston-martin', 'domain': 'astonmartin.com', 'description': '007 제임스 본드의 차. DB11과 Vantage의 영국 GT 감성', 'scores': {'performance': 90, 'reliability': 68, 'brand_value': 88, 'value_for_money': 40}},
            {'name': '재규어', 'slug': 'jaguar', 'domain': 'jaguar.com', 'description': '영국 스포츠 세단의 전통. F-TYPE과 XF, 현재 전동화 전환 중', 'scores': {'performance': 82, 'reliability': 65, 'brand_value': 78, 'value_for_money': 60}},
            {'name': '마세라티', 'slug': 'maserati', 'domain': 'maserati.com', 'description': '이탈리아 GT의 귀족. 기블리와 르반떼의 삼지창, 감성적 드라이빙', 'scores': {'performance': 85, 'reliability': 62, 'brand_value': 82, 'value_for_money': 50}},
            {'name': '랜드로버', 'slug': 'land-rover', 'domain': 'landrover.com', 'description': '오프로드의 제왕. 디펜더와 레인지로버, 극한 환경의 상징', 'scores': {'performance': 78, 'reliability': 62, 'brand_value': 82, 'value_for_money': 55}},
            {'name': 'MINI', 'slug': 'mini', 'domain': 'mini.com', 'description': 'BMW 산하 소형차의 아이콘. 쿠퍼 S의 고카트 필링, 도시형 프리미엄', 'scores': {'performance': 72, 'reliability': 70, 'brand_value': 75, 'value_for_money': 65}},
            # B티어 추가 — 오프로드/스포츠/실용
            {'name': '지프', 'slug': 'jeep', 'domain': 'jeep.com', 'description': '랭글러의 오프로드 전설. 미국식 SUV 문화의 원조', 'scores': {'performance': 72, 'reliability': 65, 'brand_value': 72, 'value_for_money': 68}},
            {'name': '스바루', 'slug': 'subaru', 'domain': 'subaru.com', 'description': '수평대향 엔진과 대칭형 AWD. WRX의 랠리 DNA, 눈길의 왕자', 'scores': {'performance': 75, 'reliability': 82, 'brand_value': 60, 'value_for_money': 72}},
            {'name': '포드', 'slug': 'ford', 'domain': 'ford.com', 'description': '머스탱과 F-150의 미국. 포드 GT로 르망을 제패한 역사', 'scores': {'performance': 78, 'reliability': 72, 'brand_value': 72, 'value_for_money': 75}},
        ],
    },
    # ============================================================
    # 향수 계급도
    # ============================================================
    {
        'name': '향수',
        'slug': 'perfume',
        'icon': '🧴',
        'group': 'lifestyle',
        'description': '향수 브랜드 계급도 - 조향 퀄리티와 커뮤니티 평판 기반',
        'display_order': 7,
        'display_config': {
            'color': '#7C3AED',
            'heroTitle': '향수 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '향수 커뮤니티 평판과 전문 리뷰를 바탕으로 S~D 티어로 분류된 향수 브랜드 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 향수 찾기',
            'stats': {'modelCount': '55+', 'reviewCount': '3,500+', 'brandCount': '18'},
        },
        'brand_score_definitions': [
            {'key': 'scent_quality', 'label': '향 퀄리티', 'weight': 30},
            {'key': 'longevity', 'label': '지속력', 'weight': 25},
            {'key': 'brand_prestige', 'label': '브랜드 위상', 'weight': 25},
            {'key': 'value', 'label': '가성비', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'scent_quality', 'label': '향 퀄리티', 'weight': 30},
            {'key': 'longevity', 'label': '지속력', 'weight': 25},
            {'key': 'sillage', 'label': '잔향/확산력', 'weight': 20},
            {'key': 'value', 'label': '가성비', 'weight': 25},
        ],
        'spec_definitions': [
            {'key': 'concentration', 'label': '농도', 'type': 'text'},
            {'key': 'volume', 'label': '용량', 'unit': 'ml', 'type': 'number'},
            {'key': 'top_note', 'label': '탑노트', 'type': 'text'},
            {'key': 'heart_note', 'label': '미들노트', 'type': 'text'},
            {'key': 'base_note', 'label': '베이스노트', 'type': 'text'},
            {'key': 'perfumer', 'label': '조향사', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'edp', 'label': 'EDP (오 드 퍼퓸)'},
                {'value': 'edt', 'label': 'EDT (오 드 뚜왈렛)'},
                {'value': 'parfum', 'label': '퍼퓸/엑스트레'},
                {'value': 'cologne', 'label': '코롱'},
                {'value': 'niche', 'label': '니치 향수'},
            ],
            'usage': [
                {'value': 'daily', 'label': '데일리'},
                {'value': 'office', 'label': '오피스'},
                {'value': 'date', 'label': '데이트'},
                {'value': 'formal', 'label': '포멀/행사'},
                {'value': 'summer', 'label': '여름용'},
                {'value': 'winter', 'label': '겨울용'},
            ],
        },
        'brands': [
            # S티어
            {'name': '메종 프란시스 커정', 'slug': 'maison-francis-kurkdjian', 'domain': 'maisonfranciskurkdjian.com', 'description': '바카라 루즈 540으로 전 세계를 사로잡은 니치 향수의 아이콘. 프란시스 커정의 천재적 조향', 'scores': {'scent_quality': 96, 'longevity': 90, 'brand_prestige': 95, 'value': 55}},
            {'name': '톰 포드', 'slug': 'tom-ford', 'domain': 'tomford.com', 'description': '럭셔리 향수의 대명사. 우드 계열과 오리엔탈 향의 관능적 해석, Private Blend의 프리미엄', 'scores': {'scent_quality': 92, 'longevity': 88, 'brand_prestige': 95, 'value': 58}},
            {'name': '르 라보', 'slug': 'le-labo', 'domain': 'lelabofragrances.com', 'description': '상탈 33의 뉴욕 감성. 핸드메이드 향수 문화를 만든 니치 향수 브랜드의 선두주자', 'scores': {'scent_quality': 94, 'longevity': 85, 'brand_prestige': 92, 'value': 60}},
            # A티어
            {'name': '딥티크', 'slug': 'diptyque', 'domain': 'diptyqueparis.com', 'description': '필로시코스와 도손의 파리 감성. 캔들로 시작해 향수까지, 프랑스 니치의 대표', 'scores': {'scent_quality': 88, 'longevity': 78, 'brand_prestige': 88, 'value': 65}},
            {'name': '바이레도', 'slug': 'byredo', 'domain': 'byredo.com', 'description': '집시 워터, 블랑쉬의 미니멀 향. 스웨덴 출신 벤 고햄의 모던 니치 브랜드', 'scores': {'scent_quality': 88, 'longevity': 80, 'brand_prestige': 85, 'value': 62}},
            {'name': '조 말론', 'slug': 'jo-malone', 'domain': 'jomalone.com', 'description': '레이어링의 원조. 영국 감성의 깔끔한 향, 입문용부터 선물용까지 대중적 니치', 'scores': {'scent_quality': 82, 'longevity': 65, 'brand_prestige': 85, 'value': 70}},
            {'name': '크리드', 'slug': 'creed', 'domain': 'creedboutique.com', 'description': '아벤투스의 전설. 250년 역사의 왕실 납품 향수 하우스, 남성 향수의 성지', 'scores': {'scent_quality': 92, 'longevity': 92, 'brand_prestige': 90, 'value': 48}},
            {'name': '샤넬', 'slug': 'chanel-perfume', 'domain': 'chanel.com', 'description': 'No.5의 전설. 블루 드 샤넬/코코 마드모아젤 등 대중과 럭셔리를 모두 잡은 하우스', 'scores': {'scent_quality': 85, 'longevity': 82, 'brand_prestige': 95, 'value': 68}},
            # B티어
            {'name': '디올', 'slug': 'dior-perfume', 'domain': 'dior.com', 'description': '소바쥬의 대중적 성공. 미스 디올부터 소바쥬까지 남녀 모두에게 사랑받는 하우스', 'scores': {'scent_quality': 82, 'longevity': 80, 'brand_prestige': 88, 'value': 72}},
            {'name': '에르메스', 'slug': 'hermes-perfume', 'domain': 'hermes.com', 'description': '떼르 데르메스와 정원 시리즈. 장 클로드 엘레나의 예술적 조향, 향수계의 에르메스', 'scores': {'scent_quality': 88, 'longevity': 72, 'brand_prestige': 92, 'value': 62}},
            {'name': '이솝', 'slug': 'aesop-perfume', 'domain': 'aesop.com', 'description': '마라케시 인텐스와 타싯의 자연주의 향. 호주 스킨케어 브랜드의 향수 라인', 'scores': {'scent_quality': 82, 'longevity': 72, 'brand_prestige': 78, 'value': 68}},
            {'name': '베르사체', 'slug': 'versace-perfume', 'domain': 'versace.com', 'description': '에로스와 딜런 블루의 대중적 인기. 화려하고 강렬한 이탈리아 감성의 향', 'scores': {'scent_quality': 75, 'longevity': 82, 'brand_prestige': 78, 'value': 80}},
            {'name': '불가리', 'slug': 'bvlgari-perfume', 'domain': 'bulgari.com', 'description': '옴니아와 아쿠아 시리즈. 이탈리안 주얼리 하우스의 세련된 향수 라인', 'scores': {'scent_quality': 78, 'longevity': 75, 'brand_prestige': 82, 'value': 72}},
            # C티어
            {'name': '캘빈 클라인', 'slug': 'calvin-klein', 'domain': 'calvinklein.com', 'description': 'CK One으로 유니섹스 향수를 개척. 이터니티/옵세션 등 90년대 아이코닉 향수들', 'scores': {'scent_quality': 68, 'longevity': 65, 'brand_prestige': 68, 'value': 88}},
            {'name': '돌체앤가바나', 'slug': 'dolce-gabbana', 'domain': 'dolcegabbana.com', 'description': '라이트 블루의 여름 대표 향. 더 원 시리즈의 따뜻한 남성 향수', 'scores': {'scent_quality': 72, 'longevity': 70, 'brand_prestige': 72, 'value': 78}},
            {'name': '휴고 보스', 'slug': 'hugo-boss', 'domain': 'hugoboss.com', 'description': '보스 보틀드의 직장인 필수템. 무난하고 깔끔한 오피스 향수의 대표', 'scores': {'scent_quality': 68, 'longevity': 68, 'brand_prestige': 65, 'value': 82}},
            # D티어
            {'name': '다비도프', 'slug': 'davidoff', 'domain': 'zinodavidoff.com', 'description': '쿨 워터의 90년대 추억. 과거의 영광에 비해 현재는 라인업 축소', 'scores': {'scent_quality': 60, 'longevity': 62, 'brand_prestige': 52, 'value': 85}},
            {'name': '플레이보이', 'slug': 'playboy-perfume', 'domain': 'playboy.com', 'description': '저가 향수 라인. 입문용으로는 가능하나 향의 깊이와 지속력에서 한계', 'scores': {'scent_quality': 38, 'longevity': 40, 'brand_prestige': 30, 'value': 90}},
        ],
    },
    # ============================================================
    # 커피 프랜차이즈 계급도
    # ============================================================
    {
        'name': '커피 프랜차이즈',
        'slug': 'coffee',
        'icon': '☕',
        'group': 'food',
        'description': '커피 프랜차이즈 계급도 - 맛/가격/접근성 기반',
        'display_order': 8,
        'display_config': {
            'color': '#78350F',
            'heroTitle': '커피 프랜차이즈 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 반응과 전문 리뷰를 바탕으로 S~D 티어로 분류된 커피 프랜차이즈 순위표',
            'itemLabel': '프랜차이즈',
            'quizCTA': '나에게 맞는 커피 찾기',
            'stats': {'modelCount': '45+', 'reviewCount': '4,000+', 'brandCount': '15'},
        },
        'brand_score_definitions': [
            {'key': 'taste', 'label': '맛/퀄리티', 'weight': 35},
            {'key': 'price', 'label': '가격 경쟁력', 'weight': 25},
            {'key': 'accessibility', 'label': '접근성/매장 수', 'weight': 20},
            {'key': 'ambiance', 'label': '매장 분위기', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'taste', 'label': '맛', 'weight': 35},
            {'key': 'price', 'label': '가격', 'weight': 25},
            {'key': 'size', 'label': '양', 'weight': 20},
            {'key': 'value', 'label': '가성비', 'weight': 20},
        ],
        'spec_definitions': [
            {'key': 'price_americano', 'label': '아메리카노 가격', 'unit': '원', 'type': 'number'},
            {'key': 'size', 'label': '기본 사이즈', 'unit': 'ml', 'type': 'number'},
            {'key': 'bean_origin', 'label': '원두 산지', 'type': 'text'},
            {'key': 'roast', 'label': '로스팅', 'type': 'text'},
            {'key': 'store_count', 'label': '매장 수', 'unit': '개', 'type': 'number'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'espresso', 'label': '에스프레소 계열'},
                {'value': 'drip', 'label': '드립/핸드드립'},
                {'value': 'cold_brew', 'label': '콜드브루'},
                {'value': 'latte', 'label': '라떼/밀크'},
                {'value': 'specialty', 'label': '시그니처/스페셜티'},
                {'value': 'non_coffee', 'label': '논커피'},
            ],
            'usage': [
                {'value': 'daily', 'label': '매일 마시는'},
                {'value': 'treat', 'label': '가끔 특별하게'},
                {'value': 'study', 'label': '공부/작업'},
                {'value': 'takeout', 'label': '테이크아웃'},
                {'value': 'meeting', 'label': '미팅/약속'},
            ],
        },
        'brands': [
            # S티어
            {'name': '블루보틀', 'slug': 'blue-bottle', 'domain': 'bluebottlecoffee.com', 'description': '스페셜티 커피의 상징. 싱글 오리진 원두와 정교한 추출, 미니멀한 매장 경험', 'scores': {'taste': 95, 'price': 45, 'accessibility': 55, 'ambiance': 95}},
            {'name': '스타벅스 리저브', 'slug': 'starbucks-reserve', 'domain': 'starbucks.com', 'description': '스타벅스의 프리미엄 라인. 리저브 바와 로스터리의 최상급 원두와 경험', 'scores': {'taste': 90, 'price': 50, 'accessibility': 65, 'ambiance': 92}},
            # A티어
            {'name': '스타벅스', 'slug': 'starbucks', 'domain': 'starbucks.com', 'description': '글로벌 커피 1위. 한국 1,900+매장, 사이렌 오더의 편의성과 시즌 음료의 강점', 'scores': {'taste': 78, 'price': 55, 'accessibility': 98, 'ambiance': 85}},
            {'name': '폴 바셋', 'slug': 'paul-bassett', 'domain': 'paulbassett.co.kr', 'description': '바리스타 챔피언의 커피. WBC 우승자 폴 바셋의 이름을 건 프리미엄 커피', 'scores': {'taste': 88, 'price': 55, 'accessibility': 60, 'ambiance': 82}},
            {'name': '테라로사', 'slug': 'terarosa', 'domain': 'terarosa.com', 'description': '강릉에서 시작된 스페셜티 로스터리. 자체 로스팅 원두와 대형 매장의 분위기', 'scores': {'taste': 90, 'price': 52, 'accessibility': 50, 'ambiance': 88}},
            # B티어
            {'name': '투썸플레이스', 'slug': 'twosome', 'domain': 'twosome.co.kr', 'description': '케이크와 커피의 조합. 디저트 카페 포지셔닝과 넓은 매장 공간의 강점', 'scores': {'taste': 72, 'price': 60, 'accessibility': 85, 'ambiance': 78}},
            {'name': '이디야커피', 'slug': 'ediya', 'domain': 'ediya.com', 'description': '가성비 커피의 대명사. 3,500+매장으로 전국 어디서나, 합리적 가격의 기본기', 'scores': {'taste': 65, 'price': 88, 'accessibility': 95, 'ambiance': 60}},
            {'name': '할리스커피', 'slug': 'hollys', 'domain': 'hollys.co.kr', 'description': '한국 커피 프랜차이즈 1세대. 고르곤졸라 피자와 함께 성장한 카페 문화의 선구자', 'scores': {'taste': 70, 'price': 68, 'accessibility': 72, 'ambiance': 72}},
            {'name': '커피빈', 'slug': 'coffee-bean', 'domain': 'coffeebean.co.kr', 'description': 'LA에서 온 글로벌 체인. 바닐라 라떼와 아이스 블렌디드의 팬덤, 미국식 커피 문화', 'scores': {'taste': 72, 'price': 58, 'accessibility': 68, 'ambiance': 75}},
            # C티어
            {'name': '메가커피', 'slug': 'mega-coffee', 'domain': 'megacoffee.me', 'description': '초저가 대용량의 혁명. 1,500원 아메리카노와 3,000+매장의 가성비 폭풍', 'scores': {'taste': 55, 'price': 95, 'accessibility': 90, 'ambiance': 45}},
            {'name': '컴포즈커피', 'slug': 'compose', 'domain': 'composecoffee.com', 'description': 'BTS 뷔의 브랜드. 저가 커피 시장의 다크호스, 빠른 매장 확장 중', 'scores': {'taste': 55, 'price': 92, 'accessibility': 82, 'ambiance': 50}},
            {'name': '빽다방', 'slug': 'paik-coffee', 'domain': 'paikscoffee.com', 'description': '백종원의 저가 커피. 2,000원대 아메리카노와 음료 메뉴의 다양성', 'scores': {'taste': 58, 'price': 90, 'accessibility': 80, 'ambiance': 48}},
            {'name': '더벤티', 'slug': 'the-venti', 'domain': 'theventi.co.kr', 'description': '대용량의 원조. 32oz 아이스 아메리카노로 가성비 시장을 개척한 브랜드', 'scores': {'taste': 52, 'price': 88, 'accessibility': 70, 'ambiance': 45}},
            # D티어
            {'name': '매머드커피', 'slug': 'mammoth-coffee', 'domain': 'mammothexpress.co.kr', 'description': '1,500원 초저가 커피. 무인 매장 위주로 편의성은 높지만 맛의 깊이는 한계', 'scores': {'taste': 42, 'price': 95, 'accessibility': 60, 'ambiance': 30}},
            {'name': '셀프커피', 'slug': 'self-coffee', 'domain': 'selfcoffee.co.kr', 'description': '무인 커피 자판기형 매장. 가격은 최저이지만 원두 퀄리티와 경험에서 아쉬움', 'scores': {'taste': 35, 'price': 98, 'accessibility': 55, 'ambiance': 20}},
        ],
    },
    # ============================================================
    # 남자지갑 계급도
    # ============================================================
    {
        'name': '남자지갑',
        'slug': 'mens-wallet',
        'icon': '👛',
        'group': 'lifestyle',
        'description': '남자 지갑 브랜드 계급도 - 소재/디자인/가성비 기반',
        'display_order': 9,
        'display_config': {
            'color': '#44403C',
            'heroTitle': '남자지갑 계급도',
            'heroDescription': '한눈에 비교하세요',
            'heroSubDescription': '커뮤니티 반응과 전문 리뷰를 바탕으로 S~D 티어로 분류된 남자지갑 브랜드 순위표',
            'itemLabel': '브랜드',
            'quizCTA': '나에게 맞는 지갑 찾기',
            'stats': {'modelCount': '45+', 'reviewCount': '2,000+', 'brandCount': '16'},
        },
        'brand_score_definitions': [
            {'key': 'material', 'label': '소재 퀄리티', 'weight': 30},
            {'key': 'design', 'label': '디자인', 'weight': 25},
            {'key': 'brand_value', 'label': '브랜드 가치', 'weight': 25},
            {'key': 'value', 'label': '가성비', 'weight': 20},
        ],
        'score_definitions': [
            {'key': 'material', 'label': '소재', 'weight': 30},
            {'key': 'design', 'label': '디자인', 'weight': 25},
            {'key': 'durability', 'label': '내구성', 'weight': 25},
            {'key': 'value', 'label': '가성비', 'weight': 20},
        ],
        'spec_definitions': [
            {'key': 'material_type', 'label': '소재', 'type': 'text'},
            {'key': 'size', 'label': '크기', 'type': 'text'},
            {'key': 'card_slots', 'label': '카드 수납', 'unit': '칸', 'type': 'number'},
            {'key': 'coin_pocket', 'label': '동전 수납', 'type': 'text'},
            {'key': 'made_in', 'label': '제조국', 'type': 'text'},
        ],
        'filter_definitions': {
            'product_type': [
                {'value': 'bifold', 'label': '반지갑'},
                {'value': 'long', 'label': '장지갑'},
                {'value': 'card_holder', 'label': '카드홀더/지퍼'},
                {'value': 'money_clip', 'label': '머니클립'},
                {'value': 'compact', 'label': '슬림/미니'},
            ],
            'usage': [
                {'value': 'daily', 'label': '데일리'},
                {'value': 'business', 'label': '비즈니스'},
                {'value': 'gift', 'label': '선물용'},
                {'value': 'minimal', 'label': '미니멀'},
                {'value': 'luxury', 'label': '럭셔리'},
            ],
        },
        'brands': [
            # S티어
            {'name': '루이비통', 'slug': 'louis-vuitton-wallet', 'domain': 'louisvuitton.com', 'description': '모노그램의 상징. LV 지갑은 남성 럭셔리 입문의 정석, 리세일 가치도 최상위', 'scores': {'material': 90, 'design': 92, 'brand_value': 98, 'value': 50}},
            {'name': '구찌', 'slug': 'gucci-wallet', 'domain': 'gucci.com', 'description': 'GG 시그니처와 웹 스트라이프. 클래식과 트렌디를 모두 잡은 이탈리아 럭셔리', 'scores': {'material': 88, 'design': 95, 'brand_value': 95, 'value': 52}},
            {'name': '보테가 베네타', 'slug': 'bottega-veneta', 'domain': 'bottegaveneta.com', 'description': '인트레치아토 위빙의 장인정신. 로고 없이 소재로 말하는 진정한 럭셔리', 'scores': {'material': 98, 'design': 90, 'brand_value': 92, 'value': 48}},
            # A티어
            {'name': '프라다', 'slug': 'prada-wallet', 'domain': 'prada.com', 'description': '사피아노 레더의 실용적 럭셔리. 미니멀한 디자인과 뛰어난 내구성의 대명사', 'scores': {'material': 90, 'design': 85, 'brand_value': 90, 'value': 55}},
            {'name': '발렌시아가', 'slug': 'balenciaga-wallet', 'domain': 'balenciaga.com', 'description': '스트리트 럭셔리의 아이콘. 대담한 로고와 독특한 실루엣의 모던 하우스', 'scores': {'material': 82, 'design': 88, 'brand_value': 85, 'value': 55}},
            {'name': '생 로랑', 'slug': 'saint-laurent-wallet', 'domain': 'ysl.com', 'description': 'YSL 카삭드레 로고의 세련된 미니멀리즘. 남성 지갑 라인의 슬림한 디자인', 'scores': {'material': 85, 'design': 88, 'brand_value': 88, 'value': 58}},
            {'name': '몽블랑', 'slug': 'montblanc-wallet', 'domain': 'montblanc.com', 'description': '마이스터슈튁의 전통. 만년필로 시작한 장인정신이 가죽 제품에도, 비즈니스 필수', 'scores': {'material': 88, 'design': 82, 'brand_value': 82, 'value': 68}},
            # B티어
            {'name': '코치', 'slug': 'coach-wallet', 'domain': 'coach.com', 'description': '어포더블 럭셔리의 대표. 합리적 가격에 좋은 가죽 퀄리티, 선물용으로 인기', 'scores': {'material': 78, 'design': 75, 'brand_value': 72, 'value': 82}},
            {'name': '버버리', 'slug': 'burberry-wallet', 'domain': 'burberry.com', 'description': '체크 패턴의 영국 헤리티지. 빈티지 체크와 TB 모노그램의 클래식한 디자인', 'scores': {'material': 82, 'design': 78, 'brand_value': 80, 'value': 62}},
            {'name': '폴 스미스', 'slug': 'paul-smith-wallet', 'domain': 'paulsmith.com', 'description': '멀티 스트라이프의 위트. 겉은 단정하고 안은 화려한 영국식 유머의 가죽 제품', 'scores': {'material': 78, 'design': 82, 'brand_value': 72, 'value': 72}},
            {'name': '벨루티', 'slug': 'berluti', 'domain': 'berluti.com', 'description': 'LVMH의 남성 전문 하우스. 베네치아 레더의 독특한 파티나 마감이 시그니처', 'scores': {'material': 92, 'design': 85, 'brand_value': 78, 'value': 45}},
            # C티어
            {'name': '타미 힐피거', 'slug': 'tommy-hilfiger-wallet', 'domain': 'tommy.com', 'description': '아메리칸 캐주얼의 대표. 합리적 가격의 기본에 충실한 남성 지갑 라인', 'scores': {'material': 62, 'design': 65, 'brand_value': 62, 'value': 85}},
            {'name': '캘빈 클라인', 'slug': 'calvin-klein-wallet', 'domain': 'calvinklein.com', 'description': 'CK 로고의 심플한 디자인. 입문~중급 가격대의 무난한 일상 지갑', 'scores': {'material': 60, 'design': 62, 'brand_value': 60, 'value': 85}},
            {'name': '닥스', 'slug': 'daks-wallet', 'domain': 'daks.com', 'description': '영국 왕실 납품 브랜드. 체크 패턴이 특징인 중장년층 선호 가죽 제품', 'scores': {'material': 72, 'design': 58, 'brand_value': 55, 'value': 75}},
            # D티어
            {'name': '금강', 'slug': 'kumkang-wallet', 'domain': 'kumkang.com', 'description': '국내 가죽 제품 전통 브랜드. 합리적 가격이지만 디자인과 브랜드 인지도에서 아쉬움', 'scores': {'material': 60, 'design': 45, 'brand_value': 38, 'value': 82}},
            {'name': '랜드리버', 'slug': 'landrover-wallet', 'domain': 'landriver.co.kr', 'description': '국내 저가 가죽 브랜드. 가격은 착하지만 소재와 마감에서 한계가 뚜렷', 'scores': {'material': 45, 'design': 40, 'brand_value': 30, 'value': 85}},
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
