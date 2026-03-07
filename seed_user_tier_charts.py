"""Seed data for user tier charts (내가 만든 계급도)"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from tiers.models import UserTierChart, TierChartComment

User = get_user_model()

# 시드 유저 생성
seed_users = {}
nicknames = {
    '라면러버': 'ramen_lover@seed.com',
    '카페인중독': 'caffeine@seed.com',
    '야식킹': 'nightsnack@seed.com',
    '혼밥러': 'solo_eater@seed.com',
}

for nickname, email in nicknames.items():
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],
            'first_name': nickname,
        }
    )
    if created:
        user.set_password('seed1234!')
        user.save()
    seed_users[nickname] = user

# 계급도 데이터
charts_data = [
    {
        'slug': 'ramen-tier',
        'title': '라면 계급도',
        'description': '대한민국 라면 순위! 여러분의 의견은?',
        'user': seed_users['라면러버'],
        'tier_data': {
            'S': [
                {'name': '신라면', 'reason': '한국 라면의 자존심. 매운맛의 정석'},
                {'name': '안성탕면', 'reason': '깊은 국물 맛의 정석. 순한맛 대표'},
                {'name': '진라면 매운맛', 'reason': '가성비 최고 매운맛 라면'},
            ],
            'A': [
                {'name': '삼양라면', 'reason': '50년 전통의 원조 라면'},
                {'name': '너구리', 'reason': '다시마 국물의 깊은 맛'},
                {'name': '짜파게티', 'reason': '한국식 짜장면의 대표'},
            ],
            'B': [
                {'name': '팔도비빔면', 'reason': '여름 별미 비빔면 1위'},
                {'name': '참깨라면', 'reason': '고소한 맛이 일품'},
                {'name': '오뚜기 진짬뽕', 'reason': '짬뽕 라면의 새 지평'},
            ],
            'C': [
                {'name': '컵누들', 'reason': '간편하지만 양이 아쉬움'},
                {'name': '튀김우동', 'reason': '무난하지만 특별함 부족'},
                {'name': '왕뚜껑', 'reason': '큰 용량이지만 맛이 평범'},
            ],
            'D': [
                {'name': '도시락 컵라면', 'reason': '추억의 맛이지만 요즘은...'},
                {'name': '김치라면', 'reason': '김치맛이 어중간'},
            ],
        },
        'view_count': 1420,
        'like_count': 128,
        'comment_count': 3,
        'is_featured': True,
    },
    {
        'slug': 'coffee-franchise-tier',
        'title': '커피 프랜차이즈 순위',
        'description': '한국 커피 프랜차이즈 티어! 당신의 최애 카페는?',
        'user': seed_users['카페인중독'],
        'tier_data': {
            'S': [
                {'name': '스타벅스', 'reason': '글로벌 브랜드 파워. 어디서나 일정한 품질'},
                {'name': '블루보틀', 'reason': '스페셜티 커피의 끝판왕'},
            ],
            'A': [
                {'name': '투썸플레이스', 'reason': '디저트와 커피 모두 수준급'},
                {'name': '폴바셋', 'reason': '바리스타 챔피언의 커피'},
                {'name': '할리스', 'reason': '넓은 매장과 안정적 맛'},
            ],
            'B': [
                {'name': '이디야', 'reason': '가성비 좋은 동네 카페'},
                {'name': '메가커피', 'reason': '대용량 저가 커피의 선두'},
                {'name': '컴포즈커피', 'reason': '저가 시장의 강자'},
            ],
            'C': [
                {'name': '빽다방', 'reason': '백종원의 저가 커피'},
                {'name': '더벤티', 'reason': '대용량이지만 맛이 아쉬움'},
            ],
            'D': [
                {'name': '자판기 커피', 'reason': '그래도 가끔 생각나는 맛'},
            ],
        },
        'view_count': 890,
        'like_count': 95,
        'comment_count': 2,
        'is_featured': True,
    },
    {
        'slug': 'delivery-app-tier',
        'title': '배달앱 순위',
        'description': '배달앱 어디가 최고? 사용 편의성, 혜택, 배달 속도 종합 평가!',
        'user': seed_users['야식킹'],
        'tier_data': {
            'S': [
                {'name': '배달의민족', 'reason': 'UI/UX 최강. 다양한 이벤트와 멤버십'},
            ],
            'A': [
                {'name': '쿠팡이츠', 'reason': '로켓배달 속도가 압도적'},
                {'name': '요기요', 'reason': '할인 쿠폰이 많고 사용이 편리'},
            ],
            'B': [
                {'name': '위메프오', 'reason': '가격 할인은 좋지만 가맹점이 적음'},
                {'name': '카카오톡 주문하기', 'reason': '카톡 연동은 편하지만 기능 부족'},
            ],
            'C': [
                {'name': '배달특급', 'reason': '수수료 없지만 인지도 부족'},
                {'name': '땡겨요', 'reason': '신생 앱. 아직 성장 중'},
            ],
            'D': [
                {'name': '네이버 주문', 'reason': '배달 전문앱 대비 기능 부족'},
            ],
        },
        'view_count': 654,
        'like_count': 67,
        'comment_count': 2,
        'is_featured': True,
    },
    {
        'slug': 'convenience-store-dosirak-tier',
        'title': '편의점 도시락 티어',
        'description': '편의점 도시락 순위! 가성비부터 맛까지 종합 평가',
        'user': seed_users['혼밥러'],
        'tier_data': {
            'S': [
                {'name': 'GS25 혜자도시락', 'reason': '가성비의 끝판왕. 이름값 하는 도시락'},
                {'name': 'CU 백종원 도시락', 'reason': '백종원 레시피의 힘. 맛 보장'},
            ],
            'A': [
                {'name': '세븐일레븐 도시락', 'reason': '종류가 다양하고 퀄리티 안정적'},
                {'name': 'CU 연어 도시락', 'reason': '연어 퀄리티가 편의점 치고 놀라움'},
            ],
            'B': [
                {'name': 'GS25 김치볶음밥', 'reason': '간편하고 무난한 선택'},
                {'name': '이마트24 도시락', 'reason': '노브랜드 감성. 양은 넉넉'},
            ],
            'C': [
                {'name': '미니스톱 도시락', 'reason': '매장이 적어서 접근성 부족'},
                {'name': '삼각김밥 세트', 'reason': '도시락이라 하기엔 좀...'},
            ],
            'D': [
                {'name': '무명 편의점 도시락', 'reason': '브랜드 없는 도시락은 리스크'},
            ],
        },
        'view_count': 432,
        'like_count': 54,
        'comment_count': 2,
        'is_featured': True,
    },
]

# 계급도 생성
for data in charts_data:
    user = data.pop('user')
    chart, created = UserTierChart.objects.update_or_create(
        slug=data['slug'],
        defaults={**data, 'user': user},
    )
    action = 'Created' if created else 'Updated'
    print(f'{action}: {chart.title} (/{chart.slug})')

# 댓글 생성
comments_data = [
    ('ramen-tier', '면덕후', '신라면이 S티어 맞죠! 역시 국민라면!'),
    ('ramen-tier', '라면은진리', '삼양라면이 A티어라니... 최소 S급인데'),
    ('ramen-tier', '야식킹', '팔도비빔면은 여름에 S급 아닌가요?'),
    ('coffee-franchise-tier', '아메리카노중독', '블루보틀 S는 인정! 맛은 확실히 다름'),
    ('coffee-franchise-tier', '가성비킹', '메가커피가 B라고? 가격 대비 최고인데!'),
    ('delivery-app-tier', '배달고수', '배민 S티어 이의없음. UI가 압도적'),
    ('delivery-app-tier', '쿠팡팬', '쿠팡이츠 로켓배달은 진짜 빠름. S급 가능!'),
    ('convenience-store-dosirak-tier', '편의점마니아', '혜자도시락 진짜 가성비 최고! S티어 확정'),
    ('convenience-store-dosirak-tier', '혼밥전문가', '백종원 도시락 퀄리티가 점점 좋아지고 있어요'),
]

for chart_slug, nickname, content in comments_data:
    chart = UserTierChart.objects.get(slug=chart_slug)
    # 댓글 유저는 기존 시드 유저 중 하나 사용
    comment_user = seed_users.get(nickname)
    if not comment_user:
        comment_user, _ = User.objects.get_or_create(
            email=f'{nickname}@comment.seed.com',
            defaults={
                'username': f'comment_{nickname}',
                'first_name': nickname,
            }
        )
        if _:
            comment_user.set_password('seed1234!')
            comment_user.save()

    TierChartComment.objects.get_or_create(
        tier_chart=chart,
        content=content,
        defaults={'user': comment_user},
    )

print('\nSeed completed!')
