"""
게시판 시드 데이터 생성 커맨드.
카테고리별 게시글·댓글을 자동 생성하여 첫 방문 시 빈 페이지를 방지합니다.
사용: python manage.py seed_posts [--category camera] [--clear]
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from brands.models import Category
from models_app.models import Product, Post, PostComment

User = get_user_model()

# ============================================================================
# 시드용 유저 (닉네임만)
# ============================================================================
SEED_USERS = [
    '사진쟁이', '카메라덕후', '렌즈수집가', '풍경헌터', '스냅러버',
    '야경마니아', '브이로거찐', '필름감성', '초보사진가', '인스타그래머',
    '여행포토', '장비충', '가성비매니아', '프로포토그래퍼', '동영상작가',
]

# ============================================================================
# 카메라 게시판 시드 데이터
# ============================================================================
CAMERA_POSTS = [
    # ── 제품 후기 (product_review) ──
    {
        'tag': 'product_review',
        'product_slug': 'sony-a7m4',
        'title': '소니 A7 IV 1년 사용기 - 만능 카메라의 정석',
        'content': '''소니 A7 IV 구매한 지 1년 됐습니다. 결론부터 말하면, 이 가격대 최고의 올라운더입니다.

장점:
- 3300만 화소로 크롭해도 충분한 해상도
- 리얼타임 트래킹 AF가 정말 미쳤습니다. 눈AF 한번 잡으면 안 놓쳐요
- 4K 60p 촬영 가능 (1.5배 크롭이지만)
- 배터리 NP-FZ100 정말 오래감

단점:
- 롤링셔터가 좀 있어요 (영상 촬영 시)
- EVF가 369만 화소인데 A7R V (944만)랑 비교하면 아쉬움
- 바디가 좀 무거움 (658g)

여행, 인물, 풍경 다 커버 가능하고 영상도 준수합니다. 입문자보다는 중급자에게 추천합니다.''',
        'rating': 5,
        'view_count': 342,
        'like_count': 28,
    },
    {
        'tag': 'product_review',
        'product_slug': 'fujifilm-x100vi',
        'title': '후지필름 X100VI 드디어 손에 넣었습니다',
        'content': '''구하기 힘들다는 X100VI... 3개월 웨이팅 끝에 겟했습니다 ㅠㅠ

정말 예쁜 카메라입니다. 필름 시뮬레이션이 JPEG로도 충분할 정도로 색감이 좋아요.
클래식 네거티브, 노스탤지어 네가 이 카메라의 꽃입니다.

화질도 X-T5와 같은 4000만 화소 센서라 놀라울 정도로 선명하고,
IBIS(손떨림 보정) 탑재돼서 저속 셔터도 손각대로 가능합니다.

단점은... 가격이 209만원인데 리셀가가 300만원 넘는다는 거?
그리고 AF가 빅3(캐논/소니/니콘) 대비 느린 건 사실입니다.

스트릿 포토, 여행용으로는 현존 최고의 카메라라고 생각합니다.''',
        'rating': 5,
        'view_count': 567,
        'like_count': 45,
    },
    {
        'tag': 'product_review',
        'product_slug': 'canon-eos-r6-iii',
        'title': '캐논 R6 III 한 달 사용 후기',
        'content': '''R6 II에서 넘어왔는데 확실히 체감됩니다.

AF 성능이 크게 향상됐고 특히 피사체 인식이 빨라졌어요.
사람, 동물, 차량 다 잘 잡아줍니다. 어두운 곳에서도 AF 정확도가 높아요.

고감도 노이즈 처리도 좋아서 ISO 12800까지는 쓸만합니다.
4K 120p도 지원하는데 화질이 꽤 괜찮습니다.

바디 그립감이 캐논답게 좋고, RF 렌즈 생태계가 워낙 탄탄해서
렌즈 선택지가 많은 게 최대 장점입니다.

가격이 좀 있지만 웨딩/행사 촬영하시는 분들께 강추합니다.''',
        'rating': 4,
        'view_count': 234,
        'like_count': 19,
    },
    {
        'tag': 'product_review',
        'product_slug': 'nikon-zf',
        'title': '니콘 Zf 디자인에 반해서 샀는데 성능도 좋네요',
        'content': '''레트로 디자인 보고 충동구매했는데 후회 없습니다.

FM2 디자인을 계승한 다이얼 조작이 정말 매력적이에요.
셔터 속도, ISO 다이얼을 물리적으로 조작하는 맛이 있습니다.

센서는 Z5 II와 같은 2450만 화소인데 ISO 성능이 뛰어나서
야경 찍을 때 진가를 발휘합니다. IBIS 8스탑도 대단하고요.

무게가 710g으로 풀프레임치곤 적당하고,
Z 마운트 렌즈들 화질이 정말 좋습니다 (특히 Z 50mm f/1.8S).

아쉬운 점은 듀얼 카드슬롯이 SD+MicroSD라는 것. 왜 CFexpress를 안 넣었을까...''',
        'rating': 5,
        'view_count': 412,
        'like_count': 35,
    },
    {
        'tag': 'product_review',
        'product_slug': 'ricoh-gr-iiix',
        'title': 'GR IIIx 포켓에 넣는 풀프레임급 화질',
        'content': '''정확히는 APS-C지만 화질이 풀프레임 뺨칩니다.

40mm 환산 화각이 인물+스트릿에 딱이에요.
포지티브 필름 모드로 찍으면 후보정 필요 없을 정도.

주머니에 들어가는 크기(260g!)가 최고의 장점이고,
스냅 셔터(0.8초 기동)로 순간 포착에 최적화되어 있습니다.

단점:
- AF가 느려요. 콘트라스트 AF라 어두우면 헤맵니다
- 배터리 200장 촬영이면 바닥... 보조배터리 필수
- 손떨림 보정 없음 (GR III에는 있는데 IIIx는 없음)

매일 들고다니는 EDC 카메라로는 최고입니다.''',
        'rating': 4,
        'view_count': 289,
        'like_count': 22,
    },
    {
        'tag': 'product_review',
        'product_slug': 'sony-a6700',
        'title': '소니 A6700 - APS-C의 끝판왕',
        'content': '''A6400에서 갈아탔는데 별세계네요.

AI 프로세서 탑재로 AF가 미러리스 APS-C 중 최고입니다.
동물 눈AF, 차량 인식까지 완벽하게 작동해요.

4K 120p 지원에 S-Log3도 사용 가능하고,
10bit 4:2:2로 색보정 여유가 넉넉합니다.

크롭 바디라 E 마운트 렌즈 끼면 환산 1.5배인데,
오히려 야생동물 촬영할 때 망원 효과로 유리합니다.

가격(180만원대)에 비해 성능이 압도적이라
두 번째 바디나 영상용으로 강추합니다.''',
        'rating': 5,
        'view_count': 198,
        'like_count': 15,
    },
    {
        'tag': 'product_review',
        'product_slug': 'gopro-hero13-black',
        'title': '고프로 Hero13 블랙 - 서핑용으로 최고',
        'content': '''서핑할 때 쓸 카메라로 고프로 13 샀습니다.

방수 10m에 HyperSmooth 6.0 손떨림 보정이 미쳤어요.
파도 타면서 찍어도 흔들림이 거의 없습니다.

5.3K 60fps 지원하는데 화질도 액션캠치고는 상당히 좋고,
GPS, 가속도 센서로 속도/고도 데이터도 오버레이 가능합니다.

배터리가 1시간 반 정도 가는데 좀 아쉬워요.
겨울에는 더 빨리 닳고... 여분 배터리 3개는 필수.

익스트림 스포츠 하시는 분들은 고프로가 답입니다.''',
        'rating': 4,
        'view_count': 156,
        'like_count': 12,
    },
    {
        'tag': 'product_review',
        'product_slug': 'panasonic-s5-iix',
        'title': '파나소닉 S5 IIX 영상 머신',
        'content': '''영상 위주 촬영하시는 분들, S5 IIX 진지하게 고려해보세요.

ProRes RAW 내부 녹화가 이 가격대에서 가능한 게 미쳤습니다.
6K 오픈게이트에 V-Log까지, 시네마 카메라 수준의 영상을 뽑아줍니다.

S5 II와 달리 HDMI RAW 출력에 SSD 녹화도 지원하고,
위상차 AF 탑재 후 AF 성능도 대폭 향상됐습니다.

L마운트 렌즈가 시그마/라이카와 호환되는 것도 큰 장점.
시그마 Art 렌즈 물려서 촬영하면 화질이 미쳐요.

사진보다 영상이 메인이라면 이 가격대 최고의 선택입니다.''',
        'rating': 5,
        'view_count': 178,
        'like_count': 14,
    },

    # ── 자유 토론 (free) ──
    {
        'tag': 'free',
        'title': '카메라 입문 추천 좀 해주세요 (예산 150만원)',
        'content': '''사진 찍는 게 취미가 됐는데 스마트폰으로는 한계를 느낍니다.
예산 150만원 정도로 바디+번들렌즈 세트 추천 부탁드려요.

주로 여행 가서 풍경/음식 찍고, 가끔 인물도 찍습니다.
동영상도 가끔 찍을 것 같은데... 4K는 됐으면 좋겠어요.

후지 X-T30 II vs 소니 A6400 vs 캐논 R50 중 고민하고 있는데
다른 추천도 환영합니다!''',
        'view_count': 523,
        'like_count': 8,
        'comments': [
            '소니 A6700이 조금 비싸긴 한데 AF 성능 차이가 크니까 조금 더 모아서 가시는 걸 추천합니다',
            '여행용이면 후지 추천! 색감이 이쁘고 JPEG로도 충분해서 후보정 안 해도 됩니다',
            'R50은 좀 아쉽고 R10이면 가격 대비 좋을 것 같아요',
            '저는 A6400 쓰는데 2024년에도 충분합니다. 렌즈값 아끼셔서 시그마 30mm 1.4 사세요',
        ],
    },
    {
        'tag': 'free',
        'title': '풀프레임 vs APS-C 논쟁... 2025년에도 유효한가요?',
        'content': '''최근 APS-C 카메라들 성능이 좋아지면서 (X-T5, A6700, R7 등)
풀프레임으로 갈 필요가 있나 싶기도 합니다.

A6700 AF가 A7 IV 수준이고, X-T5는 4000만 화소에 IBIS...
크롭 바디로 충분하지 않나요?

물론 고감도, 보케, 다이내믹 레인지에서 FF가 유리하지만
일반 취미 사진가에게 그 차이가 체감될까요?

경험담 공유해주세요!''',
        'view_count': 876,
        'like_count': 34,
        'comments': [
            'A3 사이즈 이상 인화 안 하면 APS-C로 충분합니다. 돈 아껴서 렌즈에 투자하세요',
            '저도 그렇게 생각했는데 FF 써보면 못 돌아갑니다... 특히 야경에서 ISO 차이가 큽니다',
            '풀프레임의 진짜 장점은 얕은 심도보다 렌즈 선택지가 훨씬 많다는 겁니다',
            '여행용은 APS-C, 작품용은 FF로 투바디 가는 게 답이라고 봅니다',
            '후지 GFX 중형포맷도 가격 많이 내려왔어요 ㅋㅋ 40R이 200만원대면 FF보다 쌀 수도',
        ],
    },
    {
        'tag': 'free',
        'title': 'RF 마운트 vs Z 마운트 vs E 마운트 - 2025 렌즈 생태계 비교',
        'content': '''카메라 바디도 중요하지만 결국 렌즈 시스템이 핵심이잖아요.

RF 마운트: 캐논 자체 렌즈가 최고, 하지만 서드파티 제한 (시그마/탐론 최근 참전)
Z 마운트: 니콘 네이티브 렌즈 화질 끝판왕, 서드파티 속속 출시
E 마운트: 가장 오래됐고 서드파티 포함 선택지 압도적

현재 시점에서 각 마운트의 렌즈 라인업 어떻게 보시나요?
특히 F2.8 줌 트리오 기준으로 비교하면?

저는 니콘 Z 24-70 f/2.8 S가 현존 최고의 표준줌이라고 생각합니다.''',
        'view_count': 654,
        'like_count': 25,
        'comments': [
            'E마운트가 아직까지는 선택지가 압도적이죠. 탐론 28-75 f/2.8 가성비가 미쳤습니다',
            'RF 렌즈는 비싸지만 성능은 확실히 좋습니다. RF 28-70 f/2L... 무겁지만 화질 미침',
            '시그마가 RF 마운트 렌즈 내놓기 시작하면서 캐논 유저들 환호 중',
        ],
    },
    {
        'tag': 'free',
        'title': '카메라 중고 거래 팁 공유합니다',
        'content': '''카메라 중고 거래를 많이 하는 편인데 팁 몇 가지 공유합니다.

1. 셔터 카운트 확인 필수
   - 미러리스는 10만 컷 이상이면 좀 소모됨
   - DSLR은 15-20만 이상이면 셔터 교체 시기

2. 센서 먼지/핫픽셀 체크
   - 조리개 f/16으로 하얀 벽 찍어보면 먼지 확인 가능
   - 장노출로 검은 화면 찍으면 핫픽셀 확인

3. AF 테스트
   - 핀 테스트 차트로 전핀/후핀 확인
   - 연속 AF로 움직이는 피사체 추적 테스트

4. 외관 체크
   - 마운트 스크래치 (렌즈 교환 빈도 파악)
   - 핫슈 마모 (플래시/마이크 사용 빈도)
   - 그립 라바 상태

5. 거래 장소
   - 카메라 전문 매장 근처에서 하면 바로 점검 가능
   - 용산/테크노마트 추천''',
        'view_count': 432,
        'like_count': 42,
        'comments': [
            '좋은 정보 감사합니다! 셔터카운트 확인하는 법은 카메라마다 다른가요?',
            '소니는 설정에서 직접 확인 가능하고, 캐논/니콘은 EOSInfo/NikonShutter 같은 프로그램 필요해요',
            '추가 팁: 영수증/박스 유무도 중요합니다. AS 받을 때 필요해요',
        ],
    },

    # ── 질문 (question) ──
    {
        'tag': 'question',
        'title': '인물 촬영용 렌즈 85mm vs 50mm 어떤 게 나을까요?',
        'content': '''인물 사진 위주로 찍으려고 단렌즈 하나 사려고 합니다.
소니 FE 마운트 기준으로

1. FE 85mm f/1.8 (약 60만원)
2. FE 50mm f/1.4 GM (약 150만원)
3. 시그마 Art 85mm f/1.4 DG DN (약 100만원)

중에 고민하고 있는데요...

실내 촬영이 많으면 50mm가 나을까요?
야외 촬영이면 85mm가 보케도 이쁘고 좋다는데.

경험자 분들 의견 부탁드립니다!''',
        'view_count': 345,
        'like_count': 11,
        'comments': [
            '85mm 1.8이 가성비로는 최고입니다. 인물 촬영 시작하기에 딱 좋아요',
            '실내가 많으면 50mm로 가세요. 85mm는 실내에서 거리가 안 나와서 불편합니다',
            '시그마 85 Art 추천합니다. 소니 85 1.8보다 보케가 훨씬 이쁘고 해상력도 좋아요. 무게만 감수하면...',
            '둘 다 사세요 ㅋㅋ 결국 둘 다 사게 됩니다',
        ],
    },
    {
        'tag': 'question',
        'title': '첫 카메라 가방 추천 부탁드려요',
        'content': '''카메라 처음 사서 가방도 사야 하는데 뭐가 좋을까요?

바디 1대 + 렌즈 2-3개 넣을 수 있는 사이즈면 좋겠고,
백팩형 vs 숄더백 중 어떤 게 편한지도 궁금합니다.

예산은 10-20만원 정도 생각하고 있어요.
피크디자인, 로우프로, 맨프로토 중에 쓰시는 분?''',
        'view_count': 189,
        'like_count': 5,
        'comments': [
            '피크디자인 에브리데이 슬링 6L 강추합니다. 바디1+렌즈2 딱 들어가요',
            '로우프로 프로택틱 BP 350 AW II 쓰는데 백팩형으로는 최고입니다',
            '처음엔 숄더백이 편해요. 렌즈 교환 빠르게 할 수 있어서',
        ],
    },
    {
        'tag': 'question',
        'title': 'RAW vs JPEG 차이가 정말 큰가요?',
        'content': '''아직 RAW 파일로 안 찍어봤는데...
JPEG만으로도 충분한 것 같은데 RAW를 꼭 써야 하나요?

후지필름 쓰는데 필름 시뮬레이션이 이뻐서 JPEG로 찍고 있거든요.
RAW 파일은 용량도 크고 라이트룸 같은 프로그램도 배워야 하고...

RAW 촬영의 실질적인 장점이 뭔지 알려주세요!''',
        'view_count': 267,
        'like_count': 9,
        'comments': [
            '후지는 솔직히 JPEG도 충분합니다 ㅋㅋ 하지만 노출 실수했을 때 RAW면 살릴 수 있어요',
            '하이라이트/섀도우 복원에서 RAW와 JPEG는 하늘과 땅 차이입니다',
            'RAW+JPEG 동시 촬영 해보세요. 평소엔 JPEG 쓰고 중요한 사진만 RAW 현상하면 됩니다',
            '화이트밸런스 잘못 맞추면 JPEG는 답이 없는데 RAW는 완벽하게 보정 가능해요',
        ],
    },
]


class Command(BaseCommand):
    help = '게시판 시드 데이터 생성 (카테고리별 게시글·댓글)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 게시글/댓글 삭제 후 재생성',
        )
        parser.add_argument(
            '--category',
            type=str,
            help='특정 카테고리만 생성 (예: camera)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('기존 게시판 데이터 삭제 중...')
            PostComment.objects.all().delete()
            Post.objects.all().delete()

        # 시드용 유저 생성/가져오기
        seed_users = []
        for nickname in SEED_USERS:
            email = f'{nickname}@seed.local'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': nickname,
                    'is_active': True,
                }
            )
            if created:
                user.set_unusable_password()
                user.save()
            seed_users.append(user)

        # 카테고리별 데이터 매핑
        data_map = {
            'camera': CAMERA_POSTS,
        }

        category_filter = options.get('category')

        for cat_slug, posts_data in data_map.items():
            if category_filter and category_filter != cat_slug:
                continue

            try:
                category = Category.objects.get(slug=cat_slug)
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'카테고리 {cat_slug}를 찾을 수 없음. 스킵')
                )
                continue

            self.stdout.write(f'\n{category.icon} {category.name} 게시글 생성 중...')

            for post_data in posts_data:
                user = random.choice(seed_users)
                comments_data = post_data.pop('comments', [])

                # 제품 연결
                product = None
                product_slug = post_data.pop('product_slug', None)
                if product_slug:
                    try:
                        product = Product.objects.get(slug=product_slug)
                    except Product.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'  제품 {product_slug} 없음, 제품 연결 스킵')
                        )

                post, created = Post.objects.update_or_create(
                    category=category,
                    title=post_data['title'],
                    defaults={
                        'user': user,
                        'tag': post_data.get('tag', 'free'),
                        'product': product,
                        'content': post_data['content'],
                        'rating': post_data.get('rating'),
                        'view_count': post_data.get('view_count', random.randint(50, 300)),
                        'like_count': post_data.get('like_count', random.randint(3, 20)),
                        'is_notice': post_data.get('is_notice', False),
                    }
                )

                # 댓글 생성
                comment_count = 0
                for comment_text in comments_data:
                    commenter = random.choice(seed_users)
                    PostComment.objects.get_or_create(
                        post=post,
                        content=comment_text,
                        defaults={'user': commenter}
                    )
                    comment_count += 1

                # 댓글 수 업데이트
                if comment_count > 0:
                    Post.objects.filter(pk=post.pk).update(comment_count=comment_count)

                action = '생성' if created else '업데이트'
                self.stdout.write(
                    f'  [{post_data.get("tag", "free")}] {post_data["title"][:30]}... {action} (댓글 {comment_count}개)'
                )

                # pop한 데이터 복원 (재실행 대비)
                post_data['comments'] = comments_data
                if product_slug:
                    post_data['product_slug'] = product_slug

        self.stdout.write(self.style.SUCCESS('\n게시판 시드 데이터 생성 완료!'))
        self.stdout.write(f'  게시글: {Post.objects.count()}개')
        self.stdout.write(f'  댓글: {PostComment.objects.count()}개')
