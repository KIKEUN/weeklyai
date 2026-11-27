# -*- coding: utf-8 -*-
"""Weekly AI 호 사양 — 이 파일 하나만 쓰면 카드뉴스·갑지가 나온다.

예시 = VOL.28 실제 배포본(2026-10-12). 새 호는 volN/cards.py 로 복사해서 고친다.
  python .claude/skills/weeklyai/scripts/make_vol.py N     → weeklyaivolN_src.html
  python .claude/skills/weeklyai/scripts/make_gabji.py N   → weeklyai_갑지_volN_src.html
  python .claude/skills/weeklyai/scripts/check_vol.py N    → 줄 길이·구조 검사
  python .claude/skills/weeklyai/scripts/build_vol.py N    → 배포본(base64 내장) 2개

소스(출처는 여기 주석에만 남긴다 — 카드에는 링크·각주를 넣지 않는다):
  - 컨셉·장 구성: 인스타 ai_freaks.kr/p/DeQjhJ9mqrM (index 1~5, 6·7은 CTA/팔로우라 제외)
  - 클로드 모션: claude.com/resources/articles/dashboards-and-motion (2026-10-08) + 공식 유튜브 en0GuyhieQk
  - Haiku 5.5: anthropic.com/claude-haiku-5-5 (2026-10-07) — 벤치마크표 캡처
  - API 크레딧: support.claude.com/en/articles/17154008 + claude.com/pricing Max 카드 캡처
  - 구글 워크스페이스: claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides
      + claude.com/claude-for-google-workspace 공식 영상(assets.claude.com/5391533e….mp4)
"""

VOL = 28
CATEGORY = 'AI트렌드'            # AI트렌드 / AI리터러시 / Copilot 소식 중 하나 (주제명 X)
TITLE = '클로드 10월 업데이트 모음'   # <title> 용
DESCRIPTION = '클로드 모션 베타, Claude Haiku 5.5, Max·Team 월간 API 크레딧, 구글 워크스페이스용 클로드. 10월 6~8일 앤트로픽 공식 발표를 정리했습니다.'

# 'plum'(VOL.28 자두빛 밤) / 'forest'(VOL.27 주말 아침) 또는 역할별 색 dict (scripts/wai.py ROLES 참고)
THEME = 'plum'

COVER = {
    'media': ('video', '표지영상'),       # ('video', 이름) → 이름.mp4 + 이름_poster.webp / ('img', 파일) / None
    'headline': ('클로드, 이번 주 바뀐 것', '업데이트 4가지'),   # 1줄 흰색, 2줄 강조색
    'dek': '모션 · Haiku 5.5 · API 크레딧 · 구글 워크스페이스',
    # 표지 영상을 위쪽 62%에 두고 아래는 배경색으로 녹인다 (세로 영상·사진이면 지워도 됨)
    'css': '''    #hcn-card-1 .cover-media-img { top: 0; bottom: auto; height: 62%; object-fit: cover; object-position: center 50%; }
    #hcn-card-1 .cover-bottom-deco { height: 58%; background: linear-gradient(180deg, rgba(13, 8, 11, 0) 0%, rgba(13, 8, 11, 0.55) 16%, rgba(13, 8, 11, 0.94) 34%, #0D080B 42%, #0D080B 100%); }''',
}

# 장 = 표지 + 아래 목록. "N가지면 딱 N장" (소개 장 포함), 마무리 장 없음.
# media: ('video', 이름) / ('sound', 이름: 소리 나는 영상, media.py --sound) / ('img', 파일, alt) / None(빈 슬롯)
# body : 문단 목록, 문단 = 줄 목록. 한 줄 한글 34자 이내, 6줄까지. 강조는 <b>.
# aspect: 공식 페이지 캡처처럼 16:9가 아닌 미디어는 원본 비율 ('1500 / 1030')
CARDS = [
    dict(media=('video', '인트로'), label='클로드 모션으로 만든 자전거 공유 설명 영상 (앤트로픽 공식 영상)',
         title='이번 주 클로드, 바뀐 것 4가지', sub='',
         body=[['앤트로픽이 10월 6일부터 사흘 동안 네 가지를 발표했습니다.',
                '1. 설명 영상을 만드는 <b>클로드 모션</b>',
                '2. 가격을 낮춘 <b>Haiku 5.5</b>',
                '3. Max·Team 요금제에 매달 들어오는 <b>API 크레딧</b>',
                '4. 구글 문서·시트·슬라이드 안에서 쓰는 <b>클로드</b>',
                '무엇이 바뀌었는지, 하나씩 같이 확인해 보겠습니다.']]),

    dict(media=('video', '모션'), label='클로드 모션 편집 화면 — 댓글로 수정 요청 후 MP4 내보내기 (앤트로픽 공식 영상)',
         title='1. 클로드 모션, 설명 영상을 만들어 줍니다', sub='',
         body=[['10월 8일 앤트로픽이 <b>클로드 모션</b>을 베타로 공개했습니다.',
                '글·차트·도형·이미지가 움직이는 짧은 설명 영상을 만들어 줍니다.',
                '영상을 그려내는 게 아니라 코드로 움직임을 짜기 때문에',
                '단어 하나, 숫자 하나, 타이밍만 따로 고칠 수 있습니다.',
                '숫자 하나 바뀌었다고 처음부터 다시 만들 일이 없다는 뜻입니다.',
                '결과물은 <b>MP4</b>로 내려받아 어도비·런웨이 등에서 이어 작업합니다.']]),

    dict(media=('img', '공식_벤치마크.webp', 'Claude Haiku 5.5 벤치마크 표 (앤트로픽 공식 페이지 캡처)'),
         label='Claude Haiku 5.5 벤치마크 표 (앤트로픽 공식 페이지 캡처)', aspect='1500 / 1030',
         title='2. Haiku 5.5, 더 싸고 더 똑똑해졌습니다', sub='',
         body=[['10월 7일 나온 <b>Haiku 5.5</b>는 앤트로픽의 가장 작고 빠른 모델입니다.',
                '100만 토큰당 입력 $0.10, 출력 $0.50으로 가격도 내렸습니다.',
                '컴퓨터 조작 평가(OSWorld 2.1)는 <b>15.7% → 72.4%</b>,',
                '터미널 코딩 평가(명령어 창 작업)는 <b>0.0% → 39.2%</b>로',
                'Haiku 4.5보다 올랐습니다. 같은 가격대의 GPT-6 Luna는',
                '각각 48.9%, 16.4%입니다. 작은 모델의 쓰임이 넓어졌습니다.']]),

    dict(media=('img', '공식_요금표.webp', 'Claude 개인 요금제 표 Free·Pro·Max — Max의 월 $100~$200 API 크레딧 항목에 빨간 박스 (claude.com 요금제 페이지 캡처)'),
         label='Claude 요금제 표 (claude.com 요금제 페이지 캡처, 빨간 박스 = API 크레딧)', aspect='1600 / 929',
         title='3. 매달 API 크레딧', sub='',
         body=[['10월 7일부터 Max·Team 구독자에게 매달 API 크레딧을 줍니다.',
                'Max는 5x가 <b>$100</b>, 20x가 <b>$200</b>입니다(위 표 빨간 박스).',
                'Team 구독은 회사나 부서가 여러 명이서 묶어서 쓰는',
                '단체 구독입니다. 팀원 1명당 <b>$20~$100</b>이고,',
                'API 등 개발용으로만 쓰이고, 잔여 토큰은 이월되지 않습니다.']]),

    dict(media=('video', '워크스페이스'), label='구글 문서·시트 옆 패널에서 클로드가 작업하는 장면 (앤트로픽 공식 영상)',
         title='4. 클로드, 구글 워크스페이스 안으로', sub='',
         body=[['10월 6일 구글 워크스페이스용 클로드 확장 프로그램이 나왔습니다.',
                '구글 문서·시트·슬라이드를 연 채로 옆 패널의 클로드에게 시킵니다.',
                '문서는 문장을 고치고, 시트는 수식·피벗 테이블·차트를 만들고,',
                '슬라이드는 쓰던 디자인에 맞춰 새로 만들어 줍니다.',
                '고치기 전에 내용을 먼저 확인을 할 수 있습니다.',
                '유료 요금제는 모두 사용 가능합니다.']]),
]

EXTRA_CSS = ''   # 그 밖의 호별 CSS (없으면 비워 둔다)

# 갑지(가로 1274×971). bg = 33:25로 자른 배경 이미지(없으면 None → 테마 그라데이션)
GABJI = {
    'bg': 'cover28.webp',
    'bg_note': '카드뉴스 1p 표지 영상(앤트로픽 공식 클로드 모션 영상 71.6초, Export·파트너 아이콘 장면)을 33:25로 크롭 → cover28.webp',
    'scrim': (0.44, 0.50, 0.66),   # 배경이 밝으면 올린다
}
