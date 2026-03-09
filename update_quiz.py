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

print('모든 퀴즈 정의 업데이트 완료!')
