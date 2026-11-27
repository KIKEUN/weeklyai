# -*- coding: utf-8 -*-
"""Weekly AI VOL.34 사양 — 이 파일 하나로 카드뉴스·갑지가 나온다.
  python .claude/skills/weeklyai/scripts/make_vol.py 34 && python .claude/skills/weeklyai/scripts/check_vol.py 34
  python .claude/skills/weeklyai/scripts/make_gabji.py 34 && python .claude/skills/weeklyai/scripts/build_vol.py 34

컨셉(지시 2026-11-23, 최종: 본문 점수는 1,276점 원점수 기준만 — 450점 환산 언급 삭제): 인스타 ai.trend.kr/p/DgAEt3jj6_b 구성·제목·영상 그대로 + 본문만 이데일리 기사로 손봄.
  "본문내용을 지금 내가 준 기사를 보고 손보라는거야", "기존 그림은 어느정도 그대로 써도 돼"
  기사: 이데일리 김현아 기자 2026-11-20 (MSN ar-AA2hNWmn) edaily.co.kr/News/Read?newsId=01361206645647688&mediaCodeNo=257
  인스타 8장(팔로우 CTA)만 버림. 본문 말투는 전문경영인·기자 브리핑 투(가이드 §9-4 C).
본문 근거: 기사 + 대시보드 원자료(vol34/원본/gh/r27.json) 직접 계산 → 기사 수치 전부 일치.
  - 450점 환산: 국어·수학 = 공통 + 선택 평균, 영어·한국사 원점수, 탐구 = 17과목 평균 × 2 (README)
  - 450 Astra·Neon / 449.6 Sol·Argon(기사엔 Argon 빠짐) / 449.3 Fable 5.2·Opus 5.5 / 445.8 Terra
  - 클로드: 원점수 1,270(1,276 중 탐구 3점 2문항, 생윤 공통 + Fable 물리1·Opus 지구2) — 인스타 영상의 '-6점'
  - 중국: Kimi K3.1 Pro 438(기사 '키미 K1 프로'는 오기) / Qwen4 Max 434.5 / DeepSeek V4.1 Flash 432.7
  - 국내: K-EXAONE 2.5 414.7(탐구 70.7 → 35.3점 차 중 29.3점) / Solar Pro 4 392.8 / Raon-1 mini preview 357.2 / Mi:dm K 3.0 Pro 352.8
  - 탐구 만점 모델 수(인스타 3장): 한국사 23, 사탐 9과목 3, 과탐 8과목 4 (37개 모델)
  - 기사 순위(3위·공동 4위·12위 등)는 대시보드 표시 모델에 따라 바뀌어 쓰지 않고 점수만 씀.
미디어 (인스타 그대로, 가이드 §9-4 B 16:9 꽉 채움):
  - 표지.webp: 인스타 1장(s01.jpg) y180 부터 크롭
  - 소개·만점·클로드·탐구·국산·마무리.mp4: 인스타 2~7장 영상 --fit16 --y 44 (720×405)
  - 그림은 인스타 영상 그대로 두고 본문을 그림 숫자(1,276점 원점수)에 맞춰 기사로 보강 (지시 2026-11-23 "매칭안되는걸로 다바꾸라했냐")
    대시보드_*.webp(450점 캡처)는 쓰지 않음. 중국 원점수: Kimi K3.1 Pro 1,204 / Qwen4 Max·DeepSeek V4.1 Flash 1017 1,174
"""

VOL = 34
CATEGORY = 'AI트렌드'
TITLE = '올해 수능, AI는 몇 점 받았을까?'
DESCRIPTION = '2027학년도 수능 문제를 국내외 AI 모델이 검색·계산기 없이 풀었습니다. 1,276점 만점 기준으로 오픈AI·구글 모델이 만점, 클로드는 6점 차, 국내 1위 K-EXAONE 2.5는 1,019점입니다.'

# 칠판: 짙은 칠판 초록 + 분필 노랑 / 채점 빨강 보조
THEME = {
    'card_top': '#1A3A31', 'card_mid': '#122A23', 'card_bot': '#0B1C17',
    'ink': '#F3F7F2', 'ink_rgb': '243, 247, 242',
    'line_rgb': '196, 222, 204', 'accent_rgb': '242, 201, 76',
    'accent': '#F2C94C', 'accent2': '#F8E3A0', 'surface_rgb': '226, 240, 230',
    'sub_rgb': '255, 138, 122', 'sub': '#FF8A7A', 'sub_light': '#FFE3DE',
    'slot_bg': '#FFFFFF', 'deep': '#07130F',
    'nav_rgb': '36, 104, 84', 'nav': '#246854', 'nav_hover': '#2C7D65',
    'shadow_rgb': '4, 12, 9', 'cover_top': '#21483D',
}

COVER = {
    'media': ('img', '표지.webp'),
    'headline': ('올해 수능,', 'AI는 몇 점 받았을까?'),
    'css': '''    #hcn-card-1 .cover-media-img { top: 0; bottom: auto; height: 62%; object-fit: cover; object-position: center 40%; }
    #hcn-card-1 .cover-bottom-deco { height: 58%; background: linear-gradient(180deg, rgba(11, 28, 23, 0) 0%, rgba(11, 28, 23, 0.55) 16%, rgba(11, 28, 23, 0.94) 34%, #0B1C17 42%, #0B1C17 100%); }''',
}

CARDS = [
    # 그림 = 인스타 영상 그대로(1,276점 원점수 화면). 본문은 그림 숫자 기준 + 기사(450점 환산) 보강 (지시 2026-11-23)
    dict(media=('video', '소개'), label='종합 점수 1,276점 만점 (2027학년도 수능 LLM 풀이 대시보드)',
         title='AI도 수능 봤습니다', sub='',
         body=['순천향대 컴퓨터소프트웨어공학과 구유겸 씨는 19일 수능 문제가 공개되자마자 국내외 AI 모델에게 같은 문제를 풀게 하고 결과를 대시보드로 공개했습니다. 검색이나 계산기 없이 모델 자체의 실력만 비교했고 공개 직후에 풀게 해 정답을 미리 익혔을 가능성도 줄였습니다. 그래프는 AI가 국어·수학 선택과목과 탐구 17과목까지 전부 풀어 얻은 원점수를 모두 더한 <b>1,276점</b> 만점 기준입니다.']),

    dict(media=('video', '만점'), label='GPT-6.2 Astra·Gemini 4 Neon 1,276점 만점 (2027학년도 수능 LLM 풀이 대시보드)',
         title='1. 전 과목 만점, 2개', sub='',
         body=['오픈AI의 <b>GPT-6.2 Astra</b>와 구글의 <b>Gemini 4 Neon</b>은 국어·수학 선택과목과 탐구 17과목까지 모든 문제를 맞혀 <b>1,276점</b> 만점을 받았습니다. 같은 회사의 GPT-6.2 Sol과 Gemini 4 Argon은 탐구에서 한 문제씩 틀려 1,273점을 받았습니다. 상위 네 자리를 모두 오픈AI와 구글 모델이 차지했습니다.']),

    dict(media=('video', '클로드'), label='Claude Fable 5.2·Opus 5.5 1,270점 (2027학년도 수능 LLM 풀이 대시보드)',
         title='2. 클로드는 6점 차', sub='',
         body=['앤트로픽의 클로드 <b>Fable 5.2</b>와 <b>Opus 5.5</b>는 <b>1,270점</b>으로 만점과 6점 차이입니다. '
               '국어·수학·영어·한국사는 모두 맞혔지만 탐구에서 3점짜리 두 문제를 놓쳤습니다. 두 모델 모두 생활과윤리에서 한 문제를 틀렸고 '
               '나머지 한 문제는 Fable이 물리1, Opus가 지구과학2였습니다.']),

    dict(media=('video', '탐구'), label='과목별 만점 모델 수 (인스타 ai.trend.kr 화면)',
         title='3. 승부처는 탐구', sub='',
         body=['과목 전체를 다 맞힌 모델 수를 세어 보면 국어 12개, 수학 14개, 영어 16개였고 한국사는 <b>23개</b>나 됐습니다. '
               '반면 사회탐구 9과목을 모두 맞힌 모델은 <b>3개</b>, 과학탐구 8과목을 모두 맞힌 모델은 <b>4개</b>뿐이었습니다. '
               '상위 6개 모델은 국어·수학·영어·한국사가 모두 만점이어서 순위는 결국 탐구에서 갈렸습니다.']),

    dict(media=('video', '국산'), label='모델별 점수표, K-EXAONE 2.5·Solar Pro 4 (2027학년도 수능 LLM 풀이 대시보드)',
         title='4. 국내 AI 1위는 엑사원', sub='',
         body=['국내 모델 가운데서는 LG AI연구원의 <b>K-EXAONE 2.5</b>가 <b>1,019점</b>으로 가장 높았고, 업스테이지 Solar Pro 4가 972점으로 뒤를 이었습니다. '
               'K-EXAONE 2.5는 수학 152점 만점을 받았지만 탐구는 850점 중 601점에 그쳤습니다. '
               '만점과의 차이 257점 가운데 249점이 탐구에서 벌어졌습니다.']),

    dict(media=('video', '마무리'), label='모델별 점수표 전체 (2027학년도 수능 LLM 풀이 대시보드)',
         title='5. 중국 AI는 수능을 어떻게 봤을까?', sub='',
         body=['중국 모델은 문샷AI의 Kimi K3.1 Pro가 1,204점, 알리바바의 Qwen4 Max와 딥시크의 DeepSeek V4.1 Flash가 1,174점을 받았습니다. '
               '다만 모델마다 개발 목적과 이미지 입력 지원 여부가 달라 이 점수만으로 AI의 경쟁력을 판단하기는 어렵습니다.']),

    # 마무리 장 (지시 2026-11-23 "그다음 페이지에다가 수능 자녀를 둔 임직원들을 위한 마무리 멘트") — 그림: 표지 인물이 두 손 모은 '수능 끝!' 이미지(사용자 제공, 원본/마무리_두손.png)
    dict(media=('img', '마무리.webp', '수능 끝이라고 적힌 칠판 앞에서 두 손을 모은 학생'), label='',
         title='수험생 가족 여러분, 고생 많으셨습니다', sub='',
         body=['올해 수능을 치른 자녀를 두신 임직원 여러분, 그동안 함께 마음 졸이며 고생 많으셨습니다. '
               '시험은 끝났지만 성적 발표와 원서 접수까지 남은 일정이 있습니다. '
               '남은 기간도 가족 모두 건강하게 잘 마무리하시길 바랍니다.']),
]

EXTRA_CSS = '''    /* 사진 칸은 16:9 고정, 미디어는 16:9 로 잘라 꽉 채움 (가이드 §9-4) */
    .slide-media-slot { background: #FFFFFF; }'''

GABJI = {
    'bg': 'cover34.webp',
    'bg_note': '인스타 1장 크롭(표지.webp)을 33:25로 → cover34.webp',
    'scrim': (0.44, 0.50, 0.66),
}
