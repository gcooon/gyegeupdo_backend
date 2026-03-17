"""퀴즈 정의 업데이트 스크립트"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from brands.models import Category

# 러닝화 퀴즈
running = Category.objects.get(slug='running-shoes')
running.quiz_definitions = [
    {
        'key': 'experience',
        'question': '러닝 경험이 어느 정도인가요?',
        'emoji': '🏃',
        'options': [
            {'value': 'beginner', 'label': '이제 막 시작', 'description': '러닝 1년 미만'},
            {'value': 'intermediate', 'label': '어느 정도 뛴다', 'description': '1-3년 러닝 경험'},
            {'value': 'advanced', 'label': '꽤 오래 뛰었다', 'description': '3년 이상 경력'},
            {'value': 'elite', 'label': '대회도 나간다', 'description': '마라톤 서브4 이상'},
        ],
    },
    {
        'key': 'usage',
        'question': '주로 어떤 용도로 신으실 건가요?',
        'emoji': '🎯',
        'options': [
            {'value': 'beginner', 'label': '입문/조깅', 'description': '가볍게 뛰기 시작'},
            {'value': 'daily', 'label': '데일리 트레이닝', 'description': '매일 꾸준히 훈련'},
            {'value': 'tempo', 'label': '속도 훈련', 'description': '인터벌, 템포런'},
            {'value': 'race', 'label': '레이스/대회', 'description': '기록 단축이 목표'},
            {'value': 'long', 'label': '장거리', 'description': '20km 이상 LSD'},
        ],
    },
    {
        'key': 'foot_type',
        'question': '발 형태가 어떤가요?',
        'emoji': '🦶',
        'options': [
            {'value': 'normal', 'label': '보통', 'description': '평범한 아치'},
            {'value': 'flat', 'label': '평발', 'description': '아치가 낮음'},
            {'value': 'high', 'label': '높은 아치', 'description': '발 아치가 높음'},
            {'value': 'wide', 'label': '발볼이 넓음', 'description': '넓은 발'},
        ],
    },
    {
        'key': 'priority',
        'question': '가장 중요하게 생각하는 것은?',
        'emoji': '⭐',
        'options': [
            {'value': 'cushion', 'label': '쿠셔닝', 'description': '푹신한 착화감'},
            {'value': 'speed', 'label': '가벼움/속도', 'description': '빠른 페이스'},
            {'value': 'stability', 'label': '안정성', 'description': '발목 지지력'},
            {'value': 'durability', 'label': '내구성', 'description': '오래 신을 수 있는'},
        ],
    },
    {
        'key': 'budget',
        'question': '예산은 어느 정도인가요?',
        'emoji': '💰',
        'options': [
            {'value': 'under_10', 'label': '10만원 이하', 'description': '가성비 위주'},
            {'value': '10_20', 'label': '10-20만원', 'description': '적당한 가격대'},
            {'value': '20_30', 'label': '20-30만원', 'description': '고성능 제품'},
            {'value': 'over_30', 'label': '30만원 이상', 'description': '최고급 제품'},
        ],
    },
]
running.save()
print('러닝화 퀴즈 업데이트 완료')

# 치킨 퀴즈
chicken = Category.objects.get(slug='chicken')
chicken.quiz_definitions = [
    {
        'key': 'flavor',
        'question': '어떤 맛을 좋아하시나요?',
        'emoji': '👅',
        'options': [
            {'value': 'original', 'label': '담백한 후라이드', 'description': '치킨 본연의 맛'},
            {'value': 'sweet', 'label': '달콤한 양념', 'description': '달콤짭짤한 맛'},
            {'value': 'spicy', 'label': '매콤한 맛', 'description': '칼칼하게 매운 맛'},
            {'value': 'garlic', 'label': '마늘/간장 맛', 'description': '감칠맛 나는 풍미'},
        ],
    },
    {
        'key': 'occasion',
        'question': '어떤 상황에서 먹으시나요?',
        'emoji': '🎉',
        'options': [
            {'value': 'alone', 'label': '혼자 먹을 때', 'description': '혼닭 타임'},
            {'value': 'couple', 'label': '연인/친구와', 'description': '2~3명이서'},
            {'value': 'party', 'label': '모임/파티', 'description': '여러 명이 함께'},
            {'value': 'meal', 'label': '식사 대용', 'description': '든든한 한 끼'},
        ],
    },
    {
        'key': 'drink',
        'question': '함께 마실 음료는?',
        'emoji': '🍺',
        'options': [
            {'value': 'beer', 'label': '맥주', 'description': '치맥은 진리'},
            {'value': 'soju', 'label': '소주', 'description': '치소도 좋지'},
            {'value': 'coke', 'label': '콜라/사이다', 'description': '탄산과 함께'},
            {'value': 'none', 'label': '음료 없이', 'description': '치킨만으로 충분'},
        ],
    },
    {
        'key': 'texture',
        'question': '선호하는 식감은?',
        'emoji': '✨',
        'options': [
            {'value': 'crispy', 'label': '바삭바삭', 'description': '크리스피한 튀김옷'},
            {'value': 'juicy', 'label': '촉촉한 육즙', 'description': '부드러운 살코기'},
            {'value': 'chewy', 'label': '쫄깃한 식감', 'description': '씹는 맛이 있는'},
            {'value': 'any', 'label': '상관없음', 'description': '맛있으면 OK'},
        ],
    },
    {
        'key': 'priority',
        'question': '가장 중요하게 생각하는 것은?',
        'emoji': '🎯',
        'options': [
            {'value': 'taste', 'label': '맛', 'description': '무조건 맛있어야'},
            {'value': 'price', 'label': '가성비', 'description': '양 대비 가격'},
            {'value': 'brand', 'label': '브랜드', 'description': '믿을 수 있는 브랜드'},
            {'value': 'speed', 'label': '배달 속도', 'description': '빨리 와야 함'},
        ],
    },
]
chicken.save()
print('치킨 퀴즈 업데이트 완료')

# 시계 퀴즈
watch = Category.objects.get(slug='mens-watch')
watch.quiz_definitions = [
    {
        'key': 'budget',
        'question': '예산은 어느 정도인가요?',
        'emoji': '💰',
        'options': [
            {'value': 'under_100', 'label': '100만원 이하', 'description': '입문용 시계'},
            {'value': '100_500', 'label': '100~500만원', 'description': '중급 브랜드'},
            {'value': '500_1000', 'label': '500~1000만원', 'description': '럭셔리 입문'},
            {'value': 'over_1000', 'label': '1000만원 이상', 'description': '하이엔드'},
        ],
    },
    {
        'key': 'style',
        'question': '선호하는 스타일은?',
        'emoji': '✨',
        'options': [
            {'value': 'classic', 'label': '클래식', 'description': '전통적인 디자인'},
            {'value': 'sporty', 'label': '스포티', 'description': '활동적인 느낌'},
            {'value': 'modern', 'label': '모던', 'description': '현대적인 디자인'},
            {'value': 'luxury', 'label': '럭셔리', 'description': '화려하고 고급스러운'},
        ],
    },
    {
        'key': 'purpose',
        'question': '주로 언제 착용하실 건가요?',
        'emoji': '📅',
        'options': [
            {'value': 'daily', 'label': '데일리', 'description': '일상에서 매일'},
            {'value': 'formal', 'label': '비즈니스/정장', 'description': '직장, 미팅용'},
            {'value': 'casual', 'label': '캐주얼/주말', 'description': '편하게 착용'},
            {'value': 'sport', 'label': '스포츠/아웃도어', 'description': '운동, 야외 활동'},
        ],
    },
    {
        'key': 'movement',
        'question': '무브먼트(동력원) 선호는?',
        'emoji': '⚙️',
        'options': [
            {'value': 'auto', 'label': '오토매틱(자동)', 'description': '기계식의 매력'},
            {'value': 'quartz', 'label': '쿼츠(배터리)', 'description': '정확하고 편리'},
            {'value': 'manual', 'label': '수동 와인딩', 'description': '클래식한 감성'},
            {'value': 'any', 'label': '상관없음', 'description': '디자인이 중요'},
        ],
    },
    {
        'key': 'size',
        'question': '선호하는 케이스 크기는?',
        'emoji': '📐',
        'options': [
            {'value': 'small', 'label': '36mm 이하', 'description': '클래식한 작은 사이즈'},
            {'value': 'medium', 'label': '37-40mm', 'description': '가장 보편적인 사이즈'},
            {'value': 'large', 'label': '41-44mm', 'description': '현대적인 큰 사이즈'},
            {'value': 'any', 'label': '상관없음', 'description': '디자인에 따라'},
        ],
    },
]
watch.save()
print('시계 퀴즈 업데이트 완료')

# 카메라 퀴즈
try:
    camera = Category.objects.get(slug='camera')
    camera.quiz_definitions = [
        {
            'key': 'experience',
            'question': '사진/영상 경험이 어느 정도인가요?',
            'emoji': '📷',
            'options': [
                {'value': 'beginner', 'label': '처음 시작해요', 'description': '스마트폰 사진만 찍어봄'},
                {'value': 'intermediate', 'label': '어느 정도 찍어요', 'description': '조리개·셔터 개념은 안다'},
                {'value': 'advanced', 'label': '꽤 오래 찍었어요', 'description': '수동 모드 촬영 가능'},
                {'value': 'pro', 'label': '전문가/직업', 'description': '촬영이 직업이거나 준프로'},
            ],
        },
        {
            'key': 'usage',
            'question': '주로 어떤 용도로 촬영하실 건가요?',
            'emoji': '🎯',
            'options': [
                {'value': 'travel', 'label': '여행/일상 기록', 'description': '가볍게 들고 다니며 스냅'},
                {'value': 'vlog', 'label': '브이로그/영상', 'description': '유튜브, 틱톡 영상 위주'},
                {'value': 'landscape', 'label': '풍경/건축', 'description': '고화질 풍경·야경 촬영'},
                {'value': 'sports', 'label': '스포츠/야생동물', 'description': '빠른 피사체 연사 촬영'},
                {'value': 'professional', 'label': '인물/웨딩/상업', 'description': '포트레이트·상업 촬영'},
                {'value': 'enthusiast', 'label': '취미로 깊게', 'description': '다양한 장르 두루두루'},
            ],
        },
        {
            'key': 'priority',
            'question': '카메라에서 가장 중요하게 생각하는 것은?',
            'emoji': '⭐',
            'options': [
                {'value': 'image_quality', 'label': '화질 최우선', 'description': '해상력·다이내믹레인지·색감'},
                {'value': 'af_performance', 'label': 'AF/연사 속도', 'description': '빠르고 정확한 초점'},
                {'value': 'portability', 'label': '휴대성/크기', 'description': '가볍고 작은 바디'},
                {'value': 'video', 'label': '동영상 성능', 'description': '4K/8K 촬영, 로그 지원'},
                {'value': 'value', 'label': '가성비', 'description': '가격 대비 성능'},
            ],
        },
        {
            'key': 'sensor',
            'question': '원하는 센서 크기가 있나요?',
            'emoji': '🔲',
            'options': [
                {'value': 'full_frame', 'label': '풀프레임', 'description': '최고 화질·보케, 크고 무거움'},
                {'value': 'apsc', 'label': 'APS-C / M4/3', 'description': '가볍고 가성비 좋은 크롭'},
                {'value': 'medium_format', 'label': '중형포맷', 'description': '풀프레임 이상의 초고화질'},
                {'value': 'dont_know', 'label': '잘 모르겠어요', 'description': '추천해주세요'},
            ],
        },
        {
            'key': 'budget',
            'question': '예산은 어느 정도인가요? (바디 기준)',
            'emoji': '💰',
            'options': [
                {'value': 'under_100', 'label': '100만원 이하', 'description': '엔트리·보급기'},
                {'value': '100_200', 'label': '100~200만원', 'description': '미드레인지'},
                {'value': '200_400', 'label': '200~400만원', 'description': '하이엔드'},
                {'value': 'over_400', 'label': '400만원 이상', 'description': '플래그십/프로'},
            ],
        },
    ]
    camera.save()
    print('카메라 퀴즈 업데이트 완료')
except Category.DoesNotExist:
    print('카메라 카테고리가 없습니다. seed_categories를 먼저 실행하세요.')

# 자동차 퀴즈
try:
    car = Category.objects.get(slug='car-brands')
    car.quiz_definitions = [
        {
            'key': 'experience',
            'question': '운전 경험이 어느 정도인가요?',
            'emoji': '🚗',
            'options': [
                {'value': 'beginner', 'label': '초보', 'description': '면허 취득 1년 미만'},
                {'value': 'normal', 'label': '일반', 'description': '1~5년 운전 경험'},
                {'value': 'experienced', 'label': '경력', 'description': '5년 이상 베테랑'},
                {'value': 'enthusiast', 'label': '마니아', 'description': '자동차가 취미이자 삶'},
            ],
        },
        {
            'key': 'usage',
            'question': '주로 어떤 용도로 사용하실 건가요?',
            'emoji': '🎯',
            'options': [
                {'value': 'commute', 'label': '출퇴근', 'description': '매일 도심 주행 위주'},
                {'value': 'family', 'label': '가족', 'description': '가족 이동·여행용'},
                {'value': 'performance', 'label': '퍼포먼스', 'description': '드라이빙의 재미를 추구'},
                {'value': 'outdoor', 'label': '아웃도어', 'description': '캠핑·오프로드 활동'},
                {'value': 'luxury', 'label': '럭셔리', 'description': '품격과 안락함이 중요'},
            ],
        },
        {
            'key': 'priority',
            'question': '차에서 가장 중요하게 생각하는 것은?',
            'emoji': '⭐',
            'options': [
                {'value': 'performance', 'label': '성능', 'description': '출력과 주행 감각'},
                {'value': 'fuel_efficiency', 'label': '연비', 'description': '기름값 부담 최소화'},
                {'value': 'safety', 'label': '안전', 'description': '충돌 안전·운전 보조 기술'},
                {'value': 'design', 'label': '디자인', 'description': '외관과 실내 인테리어'},
                {'value': 'value', 'label': '가성비', 'description': '가격 대비 옵션과 성능'},
            ],
        },
        {
            'key': 'fuel',
            'question': '선호하는 동력원은?',
            'emoji': '⛽',
            'options': [
                {'value': 'gasoline', 'label': '가솔린', 'description': '부드러운 가속과 정숙성'},
                {'value': 'diesel', 'label': '디젤', 'description': '높은 토크와 연비'},
                {'value': 'hybrid', 'label': '하이브리드', 'description': '연비와 성능의 균형'},
                {'value': 'ev', 'label': '전기차', 'description': '친환경·첨단 기술'},
                {'value': 'any', 'label': '상관없음', 'description': '동력원보다 차 자체가 중요'},
            ],
        },
        {
            'key': 'budget',
            'question': '예산은 어느 정도인가요?',
            'emoji': '💰',
            'options': [
                {'value': 'under_3000', 'label': '3000만원 이하', 'description': '소형·준중형 위주'},
                {'value': '3000_5000', 'label': '3000~5000만원', 'description': '중형 세단·SUV'},
                {'value': '5000_8000', 'label': '5000~8000만원', 'description': '준대형·프리미엄'},
                {'value': '8000_10000', 'label': '8000만~1억', 'description': '수입 프리미엄'},
                {'value': 'over_10000', 'label': '1억 이상', 'description': '럭셔리·슈퍼카'},
            ],
        },
    ]
    car.save()
    print('자동차 퀴즈 업데이트 완료')
except Category.DoesNotExist:
    print('자동차 카테고리가 없습니다. seed_categories를 먼저 실행하세요.')

# 향수 퀴즈
try:
    perfume = Category.objects.get(slug='perfume')
    perfume.quiz_definitions = [
        {
            'key': 'experience',
            'question': '향수 경험이 어느 정도인가요?',
            'emoji': '🌸',
            'options': [
                {'value': 'first', 'label': '처음', 'description': '향수를 처음 써보려 해요'},
                {'value': 'occasional', 'label': '가끔', 'description': '특별한 날에만 사용'},
                {'value': 'daily', 'label': '매일', 'description': '매일 향수를 뿌려요'},
                {'value': 'collector', 'label': '수집', 'description': '여러 향수를 수집하는 마니아'},
            ],
        },
        {
            'key': 'usage',
            'question': '주로 어떤 상황에서 사용하실 건가요?',
            'emoji': '🎯',
            'options': [
                {'value': 'daily', 'label': '데일리', 'description': '일상에서 가볍게'},
                {'value': 'office', 'label': '오피스', 'description': '직장·비즈니스 환경'},
                {'value': 'date', 'label': '데이트', 'description': '특별한 만남에'},
                {'value': 'formal', 'label': '포멀', 'description': '격식 있는 자리'},
                {'value': 'summer', 'label': '여름', 'description': '더운 날씨에 시원하게'},
                {'value': 'winter', 'label': '겨울', 'description': '추운 날씨에 따뜻하게'},
            ],
        },
        {
            'key': 'scent_preference',
            'question': '선호하는 향 계열은?',
            'emoji': '🌿',
            'options': [
                {'value': 'citrus_fresh', 'label': '시트러스·프레시', 'description': '상큼하고 깨끗한 감귤 계열'},
                {'value': 'floral', 'label': '플로럴', 'description': '장미·자스민 등 꽃향기'},
                {'value': 'woody', 'label': '우디', 'description': '샌달우드·시더 나무 향'},
                {'value': 'oriental_spicy', 'label': '오리엔탈·스파이시', 'description': '바닐라·머스크·향신료'},
                {'value': 'aquatic', 'label': '아쿠아틱', 'description': '바다·물·시원한 느낌'},
            ],
        },
        {
            'key': 'longevity',
            'question': '원하는 지속력은?',
            'emoji': '⏱️',
            'options': [
                {'value': 'light', 'label': '가볍게', 'description': '1~2시간, 은은하게'},
                {'value': 'moderate', 'label': '적당히', 'description': '3~5시간 정도'},
                {'value': 'long', 'label': '오래', 'description': '6~8시간 지속'},
                {'value': 'very_long', 'label': '매우 오래', 'description': '8시간 이상 강하게'},
            ],
        },
        {
            'key': 'budget',
            'question': '예산은 어느 정도인가요?',
            'emoji': '💰',
            'options': [
                {'value': 'under_5', 'label': '5만원 이하', 'description': '입문·드럭스토어 향수'},
                {'value': '5_15', 'label': '5~15만원', 'description': '중저가 브랜드 향수'},
                {'value': '15_30', 'label': '15~30만원', 'description': '프리미엄 브랜드'},
                {'value': 'over_30', 'label': '30만원 이상', 'description': '니치·하이엔드 향수'},
            ],
        },
    ]
    perfume.save()
    print('향수 퀴즈 업데이트 완료')
except Category.DoesNotExist:
    print('향수 카테고리가 없습니다. seed_categories를 먼저 실행하세요.')

# 커피 프랜차이즈 퀴즈
try:
    coffee = Category.objects.get(slug='coffee')
    coffee.quiz_definitions = [
        {
            'key': 'frequency',
            'question': '커피를 얼마나 자주 마시나요?',
            'emoji': '☕',
            'options': [
                {'value': 'sometimes', 'label': '가끔', 'description': '일주일에 1~2번 정도'},
                {'value': 'once_daily', 'label': '하루 1잔', 'description': '매일 한 잔은 필수'},
                {'value': 'twice_plus', 'label': '하루 2잔+', 'description': '커피 없인 못 살아요'},
            ],
        },
        {
            'key': 'taste',
            'question': '어떤 커피를 좋아하시나요?',
            'emoji': '👅',
            'options': [
                {'value': 'espresso', 'label': '진한 에스프레소', 'description': '쓴맛이 매력적인 진한 커피'},
                {'value': 'latte', 'label': '부드러운 라떼', 'description': '우유와 커피의 부드러운 조화'},
                {'value': 'cold_brew', 'label': '시원한 콜드브루', 'description': '깔끔하고 깊은 풍미'},
                {'value': 'frappuccino', 'label': '달달한 프라푸치노', 'description': '디저트 같은 달콤한 음료'},
                {'value': 'non_coffee', 'label': '논커피', 'description': '에이드·스무디·차 등'},
            ],
        },
        {
            'key': 'priority',
            'question': '카페에서 가장 중요하게 생각하는 것은?',
            'emoji': '⭐',
            'options': [
                {'value': 'taste', 'label': '맛', 'description': '커피 맛이 최우선'},
                {'value': 'price', 'label': '가격', 'description': '가성비가 중요해요'},
                {'value': 'ambiance', 'label': '매장 분위기', 'description': '인테리어·좌석 편안함'},
                {'value': 'accessibility', 'label': '접근성', 'description': '가까운 곳에 매장이 많은'},
                {'value': 'size', 'label': '사이즈', 'description': '양이 많아야 해요'},
            ],
        },
        {
            'key': 'location',
            'question': '주로 어디서 마시나요?',
            'emoji': '📍',
            'options': [
                {'value': 'dine_in', 'label': '매장에서', 'description': '카페에 앉아서 여유롭게'},
                {'value': 'takeout', 'label': '테이크아웃', 'description': '들고 이동하며'},
                {'value': 'delivery', 'label': '배달', 'description': '집이나 사무실로 배달'},
            ],
        },
        {
            'key': 'budget',
            'question': '1잔 예산은 어느 정도인가요?',
            'emoji': '💰',
            'options': [
                {'value': 'under_2000', 'label': '2000원 이하', 'description': '저가 커피 위주'},
                {'value': '2000_4000', 'label': '2000~4000원', 'description': '적당한 가격대'},
                {'value': '4000_6000', 'label': '4000~6000원', 'description': '프리미엄 프랜차이즈'},
                {'value': 'over_6000', 'label': '6000원 이상', 'description': '스페셜티 커피숍'},
            ],
        },
    ]
    coffee.save()
    print('커피 프랜차이즈 퀴즈 업데이트 완료')
except Category.DoesNotExist:
    print('커피 카테고리가 없습니다. seed_categories를 먼저 실행하세요.')

# 남자지갑 퀴즈
try:
    wallet = Category.objects.get(slug='mens-wallet')
    wallet.quiz_definitions = [
        {
            'key': 'style',
            'question': '선호하는 스타일은?',
            'emoji': '✨',
            'options': [
                {'value': 'classic', 'label': '클래식', 'description': '전통적이고 격식 있는 디자인'},
                {'value': 'modern_minimal', 'label': '모던 미니멀', 'description': '깔끔하고 세련된 심플함'},
                {'value': 'street', 'label': '스트리트', 'description': '캐주얼하고 트렌디한 감성'},
                {'value': 'vintage', 'label': '빈티지', 'description': '세월이 묻어나는 클래식한 멋'},
            ],
        },
        {
            'key': 'type',
            'question': '원하는 지갑 형태는?',
            'emoji': '👛',
            'options': [
                {'value': 'bifold', 'label': '반지갑', 'description': '가장 보편적인 접이식'},
                {'value': 'long', 'label': '장지갑', 'description': '수납력 좋은 긴 형태'},
                {'value': 'card_holder', 'label': '카드홀더', 'description': '카드 위주 슬림 수납'},
                {'value': 'money_clip', 'label': '머니클립', 'description': '지폐 고정 클립 방식'},
                {'value': 'slim', 'label': '슬림', 'description': '주머니에 넣기 편한 초박형'},
            ],
        },
        {
            'key': 'priority',
            'question': '지갑에서 가장 중요하게 생각하는 것은?',
            'emoji': '⭐',
            'options': [
                {'value': 'material', 'label': '소재 퀄리티', 'description': '가죽 품질과 마감이 중요'},
                {'value': 'design', 'label': '디자인', 'description': '보기 좋은 외관이 최고'},
                {'value': 'brand', 'label': '브랜드', 'description': '인지도 있는 브랜드 선호'},
                {'value': 'value', 'label': '가성비', 'description': '가격 대비 만족도'},
            ],
        },
        {
            'key': 'usage',
            'question': '주로 어떤 용도로 사용하실 건가요?',
            'emoji': '🎯',
            'options': [
                {'value': 'daily', 'label': '데일리', 'description': '매일 들고 다니는 용도'},
                {'value': 'business', 'label': '비즈니스', 'description': '직장·미팅 시 사용'},
                {'value': 'gift', 'label': '선물용', 'description': '소중한 사람에게 선물'},
                {'value': 'minimal', 'label': '미니멀', 'description': '최소한의 카드·현금만'},
            ],
        },
        {
            'key': 'budget',
            'question': '예산은 어느 정도인가요?',
            'emoji': '💰',
            'options': [
                {'value': 'under_10', 'label': '10만원 이하', 'description': '실용적인 가성비 제품'},
                {'value': '10_30', 'label': '10~30만원', 'description': '중급 브랜드 제품'},
                {'value': '30_50', 'label': '30~50만원', 'description': '프리미엄 브랜드'},
                {'value': '50_100', 'label': '50~100만원', 'description': '럭셔리 브랜드'},
                {'value': 'over_100', 'label': '100만원 이상', 'description': '하이엔드 명품'},
            ],
        },
    ]
    wallet.save()
    print('남자지갑 퀴즈 업데이트 완료')
except Category.DoesNotExist:
    print('남자지갑 카테고리가 없습니다. seed_categories를 먼저 실행하세요.')

print('모든 퀴즈 정의 업데이트 완료!')
