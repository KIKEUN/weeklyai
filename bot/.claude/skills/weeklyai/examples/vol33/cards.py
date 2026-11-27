# -*- coding: utf-8 -*-
"""Weekly AI VOL.33 사양 — 이 파일 하나로 카드뉴스·갑지가 나온다.
  python .claude/skills/weeklyai/scripts/make_vol.py 33 && python .claude/skills/weeklyai/scripts/check_vol.py 33
  python .claude/skills/weeklyai/scripts/make_gabji.py 33 && python .claude/skills/weeklyai/scripts/build_vol.py 33

컨셉(지시 2026-11-16): 인스타 ai.trend.kr/p/DfnnLk3j5G1 (Gemini 4 Carbon 일반 공개) 를 메인 주제로, 공식 소개 주소 확인.
  인스타 2~7장을 3가지로 묶음(성능 평가·보안·Argon/Carbon). 안전 지표 장 삭제, 쓸 수 있는 곳+가격 장은 3번에 합치고
  비교표를 직접 만들어 넣음(지시 2026-11-16 — 공식 글에 토큰·가격 비교표가 없음). 쓸 수 있는 곳+가격은 한 장.
  8~10장(DM 유도·팔로우)은 버림. 인스타 가격 카드(직접 그린 패널)·아르곤/카본 비교 카드는 쓰지 않고 공식 자료로 대체.
본문 근거 (2026-11-16 확인, 전부 구글 공식 블로그):
  - 일반 공개(2026-11-10): blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/
      유료 API(AI Studio·Gemini for business) 개발자·기업 / Google AI Ultra 구독자(Antigravity·Gemini 앱·검색 AI 모드) 순차 적용
      가격 $2 입력·$10 출력(100만 토큰), 각주: 도입 기간 2026-11-30 종료 후 $4·$20 / Argon 과 같은 도입가
      "Argon remains the ideal choice for the majority of software engineering and knowledge work" / Carbon 은 토큰을 더 씀
      /swarm (Antigravity, 프리뷰) / 과학자 6개월 무료 신청 / 에이전트 정직성 평가 92%(Argon 70%)
  - 첫 발표(2026-10-28): .../gemini-models/introducing-gemini-4-carbon/
      AA Intelligence Index v5.0 59점 1위 / SEC-bench Pro 88.2%, ExploitGym 54.8%, CWE-bench 71.0%
      Fairwind Program 으로 보안 방어 담당자에게 먼저 / Gray Swan 간접 프롬프트 인젝션 공격 성공률 0.0%(Argon 0.7%)
  - 성적표 수치: 공식 평가표 이미지(gemini_4_carbon__evals-table) — AA Index 59/58/57, AutomationBench 53.9/41.4/42.5, OSWorld-2.1 81.5/87.2
  - 안전 지표: 공식 차트(gemini_4_carbon_misalignment) — 꼼수 시도 3.6→0.4%, 성공 2.4→0.0%, 사내 사용 경고 0.078→0.016%
미디어 (전부 구글 공식):
  - 표지영상.mp4: 공식 유튜브 rOVEmjfPmYk (/swarm 에펠탑 3D 전시) 34~46초 — 인스타 표지와 같은 영상의 원본
  - 아틀란티스.mp4: 공식 유튜브 Cxf3AVX8_7I 45~57초 / 펠리컨게임.mp4: 공식 유튜브 dNbkThtNzS8 41~55초
  - 공식_성적표.webp: 공식 평가표 위쪽(종합~지식 업무 9행)만 잘라 씀 — 전체 17행은 카드에서 글자가 안 보임
  - 공식_취약점찾기.webp: 공식 블로그 이미지 그대로
  - 비교표.webp: vol33/원본/비교표.html 을 capture.py 로 캡처 (직접 만든 표, 지시 2026-11-16)
      Argon 근거: .../gemini-models/introducing-gemini-4-argon/ (2026-10-13) — Pro·Ultra 구독자(Gemini 앱·검색 AI 모드),
      도입가 $2·$10, 2026-11-30 이후 $4·$20 (Carbon 과 동일)
"""

VOL = 33
CATEGORY = 'AI트렌드'
TITLE = 'Gemini 4 Carbon 일반 공개'
DESCRIPTION = '구글이 고성능 AI 모델 Gemini 4 Carbon을 11월 10일 일반에 공개했습니다. 성능 평가, 취약점 탐지, Argon과의 차이, 가격을 구글 공식 발표 기준으로 정리했습니다.'

# Gemini 4 Carbon 키아트: 짙은 남색 밤 + 구글 블루 / 수정 결정의 청록 보조
THEME = {
    'card_top': '#0F1D40', 'card_mid': '#0A142E', 'card_bot': '#060B1C',
    'ink': '#F2F6FF', 'ink_rgb': '242, 246, 255',
    'line_rgb': '138, 180, 248', 'accent_rgb': '92, 156, 255',
    'accent': '#5C9CFF', 'accent2': '#A9CBFF', 'surface_rgb': '208, 226, 255',
    'sub_rgb': '110, 226, 222', 'sub': '#6EE2DE', 'sub_light': '#DDFBF9',
    'slot_bg': '#0B1530', 'deep': '#050915',
    'nav_rgb': '26, 72, 168', 'nav': '#1A48A8', 'nav_hover': '#2158C8',
    'shadow_rgb': '4, 8, 20', 'cover_top': '#152A5C',
}

COVER = {
    'media': ('video', '표지영상'),
    'headline': ('구글의 차세대 AI,', 'Gemini 4 Carbon 공개'),
    'dek': '성능 평가 · 보안 검증 · Argon과 차이 · 가격',
    'css': '''    #hcn-card-1 .cover-media-img { top: 0; bottom: auto; height: 62%; object-fit: cover; object-position: center 50%; }
    #hcn-card-1 .cover-bottom-deco { height: 58%; background: linear-gradient(180deg, rgba(6, 11, 28, 0) 0%, rgba(6, 11, 28, 0.55) 16%, rgba(6, 11, 28, 0.94) 34%, #060B1C 42%, #060B1C 100%); }''',
}

CARDS = [
    dict(media=('video', '아틀란티스'), label='Gemini 4 Carbon이 만든 실시간 3D 수중 도시 장면 (구글 공식 영상)',
         title='Gemini 4 Carbon이 공개되었습니다', sub='',
         body=[['구글의 고성능 AI 모델 <b>Gemini 4 Carbon</b>이',
                '10월 28일 발표에 이어, 보안 전문가의 검증 후',
                '11월 10일 일반 이용자에게 공개됐습니다.',
                '다른 AI와 비교해 어느 수준인지,',
                '왜 보안 전문가에게 먼저 공개되었는지,',
                'Argon과는 어떻게 다른지, 비용은 얼마인지 정리했습니다.']]),

    dict(media=('img', '공식_성적표.webp', 'Gemini 4 Carbon 평가표 — Carbon·Argon·GPT-6 Astra·Claude Opus 5.5·Claude Fable 5.1 비교 (구글 공식 이미지)'),
         label='Gemini 4 Carbon 평가표 중 종합·코딩·컴퓨터 조작·지식 업무 (구글 공식 이미지)',
         title='1. 종합 성능 1위, 컴퓨터 조작은 Claude 우세', sub='',
         body=[['외부 기관 Artificial Analysis 종합 지수에서 <b>59점</b>을 받았습니다.',
                'Claude Opus 5.5는 58점, GPT-6 Astra는 57점입니다.',
                '업무 자동화 평가에서는 Carbon <b>53.9%</b>, Opus 5.5 42.5%입니다.',
                '반면 컴퓨터 조작 평가에서는 Carbon 81.5%,',
                'Opus 5.5 87.2%로 Claude가 앞섰습니다.',
                '다양한 분야의 성능에서 타사의 프론티어 모델을 따라잡았습니다.']]),

    dict(media=('img', '공식_취약점찾기.webp', 'SEC-bench Pro 막대 차트 — Gemini 4 Carbon 88.2%, GPT-6 Astra 85.4%, Gemini 4 Argon 83.4% (구글 공식 이미지)'),
         label='취약점 탐지 평가 SEC-bench Pro 결과 (구글 공식 이미지)',
         title='2. 소프트웨어 취약점 탐지에서도 높은 성능', sub='',
         body=[['취약점 탐지 평가에서 Carbon은 <b>88.2%</b>를 기록했습니다.',
                'GPT-6 Astra는 85.4%, Argon은 83.4%입니다.',
                '이 능력은 해킹하려는 사람에게도 도움이 되어',
                '사이버 공격에 악용될 가능성도 있었습니다.',
                '그래서 구글은 사이버보안 전문가의 사전 검증을 거쳐,',
                '악용을 막는 장치를 보완한 뒤 일반에 공개했습니다.']]),

    # 작업당 비용: artificialanalysis.ai/models/comparisons/gemini-4-carbon-vs-gemini-4-argon (2026-11-16 확인)
    #   Cost per Task — Carbon(high) $5.48, Argon(high) $4.97 / 토큰 사용량 수치는 공식·AA 페이지 모두 없음
    dict(media=('img', '비교표.webp', 'Gemini 4 Argon과 Carbon 비교표 — 일반 공개일, 권장 업무, 개인 구독, API 가격, 작업당 비용'),
         label='Argon과 Carbon 비교 (구글 공식 발표·Artificial Analysis 수치를 표로 정리)',
         title='3. Argon과 Carbon, 어떤 업무에 적합할까?', sub='',
         body=[['구글은 일반적인 코딩·문서 업무에는 <b>Argon</b>,',
                '복잡한 코딩이나 과학 연구에는 <b>Carbon</b>을 추천합니다.',
                'Carbon은 복잡한 문제를 처리할 때',
                '토큰 사용량이 늘어 비용이 높아질 수 있습니다.',
                '두 모델의 토큰 단가는 같으며,',
                '12월 1일부터 인상이 계획되어 있습니다.']]),
]

EXTRA_CSS = '''    /* 미디어 칸은 전 장 16:9 로 통일(2p 기준, 지시 2026-11-16). 남는 여백은 각 이미지의 배경색으로 채운다 */
    #hcn-card-3 .slide-media-slot, #hcn-card-3 .slide-media-slot > img,
    #hcn-card-4 .slide-media-slot, #hcn-card-4 .slide-media-slot > img { background: #FFFFFF; }
    #hcn-card-5 .slide-media-slot, #hcn-card-5 .slide-media-slot > img { background: #0B1530; }'''

GABJI = {
    'bg': 'cover33.webp',
    'bg_note': '공식 키아트(gemini_4_carbon_key_art_16-9_lockup)를 33:25로 크롭 → cover33.webp',
    'scrim': (0.44, 0.50, 0.66),
}
