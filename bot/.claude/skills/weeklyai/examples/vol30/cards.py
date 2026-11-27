# -*- coding: utf-8 -*-
"""Weekly AI VOL.30 사양 — 이 파일 하나로 카드뉴스·갑지가 나온다 (봇 §15).
  python .claude/skills/weeklyai/scripts/make_vol.py 30 && python .claude/skills/weeklyai/scripts/check_vol.py 30
  python .claude/skills/weeklyai/scripts/make_gabji.py 30 && python .claude/skills/weeklyai/scripts/build_vol.py 30

소스(컨셉·장 구성): 인스타 ai.trend.kr/p/DevSsJ7j7bM "챗GPT에 절대 하면 안 되는 말 20가지" (img_index 1~7. 8은 댓글 CTA라 제외)
  index 1 표지 → 1p / 2 범인은 AI가 아니라 질문 → 2p 소개 / 3 "고쳐줘" → 3p / 4 요약 → 4p / 5 아이디어 → 5p / 6 비판 → 6p / 7 먼저 묻게 → 7p
  ★ 컨셉 변경(지시): "ChatGPT에게" → "AI에게" 하면 안 되는 말. AI리터러시. 특정 제품이 아니라 모든 AI 공통이라는 근거로 세 회사+MS 공식 가이드를 씀.
본문 근거 (2026-10-26 확인):
  - 앤트로픽 프롬프팅 모범 사례(한국어) platform.claude.com/docs/ko/build-with-claude/prompt-engineering/claude-prompting-best-practices
      "명확하고 직접적으로 작성하기" — 뛰어나지만 새로 입사한 직원 / "복잡한 프롬프트 체이닝" — 자기 수정: 초안 생성 → 검토 → 개선
  - 오픈AI platform.openai.com/docs/guides/prompt-engineering — "A GPT model is like a junior coworker … explicit instructions"
  - 구글 Workspace 프롬프트 작성 가이드 101(한국어) workspace.google.com/intl/ko/resources/ai/writing-effective-prompts/
      페르소나·작업·맥락·형식 / "네 가지 요소를 모두 포함할 필요는 없지만 몇 가지를 활용하면 도움" / "대화하듯이 말하세요"
  - 마이크로소프트 support.microsoft.com/ko-kr/topic/learn-about-copilot-prompts-f6c3b467… — 목표·컨텍스트·원본·기대 사항
미디어(전부 공식):
  - 표지영상·네가지요소·대화하듯: 구글 Workspace 공식 유튜브 EQQMcTBPYzo "Prompting like a Pro" 26.3~36.5 / 89~113 / 71~84.5초
  - 구체적지시·요약형식: 앤트로픽 공식 유튜브 OfUn6HjwXhI "Behind the prompt: Prompting tips for Claude.ai" 95.5~127 / 151.3~160.8초
  - 공식_명확하게·공식_자기수정: 앤트로픽 한국어 문서 화면 캡처
  - 인스타_5.webp: 원본 그림의 "내 독자층"을 "참여 직원"으로 고쳐 씀(사내용, 지시 2026-10-26)
  인스타 카드 이미지(직접 그린 비교 그림)는 쓰지 않음.
"""

VOL = 30
CATEGORY = 'AI리터러시'
TITLE = 'AI에게 하면 안 되는 말 5가지'
DESCRIPTION = '고쳐줘·요약해 줘·아이디어 내줘·더 강력하게·도와줘. 자주 쓰는 다섯 마디를 바꿔 쓸 문장과 함께. 앤트로픽·오픈AI·구글 공식 가이드 기준.'

# 테라코타: 앤트로픽 공식 영상 타이틀 카드의 점토색 (짙은 밤색 + 테라코타 / 세이지 보조)
THEME = {
    'card_top': '#2A1A14', 'card_mid': '#1C120E', 'card_bot': '#110B08',
    'ink': '#FFF4EE', 'ink_rgb': '255, 244, 238',
    'line_rgb': '236, 170, 140', 'accent_rgb': '217, 119, 87',
    'accent': '#D97757', 'accent2': '#F4B79C', 'surface_rgb': '255, 224, 210',
    'sub_rgb': '150, 190, 170', 'sub': '#96BEAA', 'sub_light': '#E4F4EC',
    'slot_bg': '#1E140F', 'deep': '#140A06',
    'nav_rgb': '120, 52, 30', 'nav': '#8A3E22', 'nav_hover': '#A04826',
    'shadow_rgb': '10, 6, 4', 'cover_top': '#33201A',
}

COVER = {
    'media': ('img', '인스타_표지.webp'),   # 인스타 index 1 사진 (위 로고·아래 제목 글자 잘라냄)
    'headline': ('AI에게 하면 안 되는 말', '5가지와 바꿔 쓸 문장'),
    'dek': '답이 별로였다면, 질문을 바꿔 볼 차례입니다',
    'css': '''    #hcn-card-1 .cover-media-img { top: 0; bottom: auto; height: 62%; object-fit: cover; object-position: center 30%; }
    #hcn-card-1 .cover-bottom-deco { height: 58%; background: linear-gradient(180deg, rgba(17, 11, 8, 0) 0%, rgba(17, 11, 8, 0.55) 16%, rgba(17, 11, 8, 0.94) 34%, #110B08 42%, #110B08 100%); }''',
}

CARDS = [
    dict(media=('img', '인스타_2.webp', '막연한 질문 "고쳐줘" → 무난한 답 / 구체적인 질문 "내 말투는 유지하면서 문제점을 찾아 고쳐줘" → 문제점 3가지'),
         label='막연한 질문과 구체적인 질문 비교 (인스타 index 2 그림)', aspect='1080 / 762',
         title='답이 별로라면, 질문부터 봅니다', sub='',
         body=[['AI의 답이 기대에 못 미쳤다면, 대개 요청이 막연했던 경우입니다.',
                'AI는 똑똑하지만 우리 일의 맥락은 모르는 신입 직원과 같습니다.',
                '신입에게 일을 줄 때처럼 목적·대상·형식·분량을 함께 알려야 합니다.',
                '앤트로픽·오픈AI·구글의 공식 가이드도 같은 점을 강조합니다.',
                '자주 쓰는 요청 다섯 가지를 바꿔 쓸 문장과 함께 정리했습니다.']]),

    dict(media=('img', '인스타_3.webp', '"군더더기와 반복을 덜고 50% 줄여줘" — 원래 글 100%, 줄인 글 50%'),
         label='군더더기와 반복을 덜고 50% 줄인 예 (인스타 index 3 그림)', aspect='1080 / 762',
         title='1. "고쳐줘", 지킬 것까지 말합니다', sub='',
         body=[['"고쳐줘"만 보내면 AI는 무엇을 남길지 몰라 글 전체를 다시 씁니다.',
                '<b>"내 말투는 유지하면서 문제점을 찾아 고쳐줘"</b>처럼',
                '남길 것과 고칠 것을 나눠서 지시하면 됩니다.',
                '분량을 줄일 때는 <b>"군더더기와 반복을 덜고 50% 줄여줘"</b>처럼',
                '목표치를 숫자로 줍니다. 수정 요청이 한두 번으로 끝납니다.']]),

    dict(media=('img', '인스타_4.webp', '"이것을 요약해 줘" 대신 "3·1·1로 요약해 줘" — 핵심 3, 결론, 추천 행동'),
         label='핵심 3·결론 1·추천 행동 1로 요약한 예 (인스타 index 4 그림)', aspect='1080 / 762',
         title='2. "요약해 줘", 모양부터 정합니다', sub='',
         body=[['"요약해 줘"만 쓰면 길이와 형식을 AI가 임의로 정합니다.',
                '<b>"핵심 3가지, 결론 1개, 추천 행동 1개로 요약해 줘"</b>처럼',
                '받고 싶은 모양을 먼저 정하면 보고서에 바로 옮길 수 있습니다.',
                '설명을 부탁할 때는 "초보자도 이해하게, 사례 포함"을 덧붙입니다.',
                '정리를 다시 하는 시간이 그만큼 줄어듭니다.']]),

    dict(media=('img', '인스타_5.webp', '"[주제] 아이디어 10가지, 참여 직원에 맞춰" — 대상: 참여 직원, 01~10'),
         label='개수와 대상을 정한 아이디어 요청 (인스타 index 5 그림)', aspect='1080 / 762',
         title='3. "아이디어 내줘", 개수와 대상을 붙입니다', sub='',
         body=[['"아이디어 내줘"에는 개수도, 누구를 위한 것인지도 빠져 있습니다.',
                '<b>"[주제] 아이디어 10가지를 참여 직원에 맞춰 줘"</b>처럼',
                '개수와 대상을 정하면 바로 검토할 수 있는 목록이 나옵니다.',
                '구글은 좋은 요청의 요소로 역할·작업·맥락·형식 네 가지를 꼽습니다.',
                '매번 다 채울 필요는 없고, 몇 가지만 넣어도 결과가 달라집니다.']]),

    dict(media=('img', '인스타_6.webp', '"비평하고 약점 3가지를 짚은 뒤 다시 써줘" — 초안 → 약점 3가지 → 개선안'),
         label='초안 → 약점 3가지 → 개선안 (인스타 index 6 그림)', aspect='1080 / 762',
         title='4. "더 강력하게", 비평부터 시킵니다', sub='',
         body=[['"더 강력하게 만들어줘"라고 하면 표현만 세지고 내용은 그대로입니다.',
                '<b>"이 버전을 비평하고 약점 3가지를 짚은 뒤 다시 써줘"</b>라고',
                '지시하면 AI가 문제를 먼저 찾고, 그다음에 고칩니다.',
                '앤트로픽 가이드도 초안 → 검토 → 개선 순서를 권합니다.',
                '"어떻게 생각해?" 대신 장점·단점·개선안으로 나눠 물어도 됩니다.',
                '중요한 보고서라면 올리기 전에 이 단계를 한 번 거치길 권합니다.']]),

    dict(media=('img', '인스타_7.webp', '"답하기 전에 나에게 질문 3개를 먼저 해줘" — 누구에게, 언제까지, 분량 → 팀장님께, 금요일까지, 한 장으로'),
         label='AI가 먼저 질문 3개를 묻는 대화 (인스타 index 7 그림)', aspect='1080 / 762',
         title='5. "이걸 도와줘", AI가 먼저 묻게 합니다', sub='',
         body=[['무엇부터 말해야 할지 모를 때는 순서를 바꾸면 됩니다.',
                '<b>"답하기 전에 맥락을 알기 위해 나에게 질문 3개를 먼저 해줘"</b>',
                'AI가 대상·마감·분량을 물어 오면 그에 답하기만 하면 됩니다.',
                '구글 가이드도 한 번에 끝내지 말고 대화하듯 다듬으라고 합니다.',
                '첫 답은 초안으로 보고, 이어지는 질문으로 완성도를 높이면 됩니다.']]),
]

# 공식 영상(16:9)은 꽉 채우고, 문서 캡처는 흰 바탕에 contain
EXTRA_CSS = '''    .slide-media-slot { background: #F0F1F3; }
    .slide-media-slot > img { object-fit: contain; background: #F0F1F3; }'''

GABJI = {
    'bg': 'cover30.webp',
    'bg_note': '인스타 index 1 사진 → 33:25 크롭 → cover30.webp',
    'scrim': (0.44, 0.50, 0.66),
}
