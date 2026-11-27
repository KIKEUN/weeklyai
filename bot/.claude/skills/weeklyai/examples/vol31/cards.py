# -*- coding: utf-8 -*-
"""Weekly AI VOL.31 사양 — 이 파일 하나로 카드뉴스·갑지가 나온다 (봇 §15).
  python .claude/skills/weeklyai/scripts/make_vol.py 31 && python .claude/skills/weeklyai/scripts/check_vol.py 31
  python .claude/skills/weeklyai/scripts/make_gabji.py 31 && python .claude/skills/weeklyai/scripts/build_vol.py 31

소스(컨셉): 인스타 ai_freaks.kr/p/DeyEtbfGkmb "클로드 듀엣" (index 1~5. 6은 팔로우 장이라 제외)
  ★ 컨셉 변경(지시 2026-11-02): 듀엣 단독 소개 → 다섯 에이전트를 기능 중심으로. 순서(지시): dots → 듀엣 → 스파크 → 그록봇 → 뮤즈
본문 근거 (2026-11-02 각 공식 소개글에서 확인):
  - 클로드 듀엣: claude.com/resources/articles/claude-duet (2026-10-21)
      Opus 5.5 / 아침 브리핑 / "every few hours" 확인 / "over 6,000 connectors and plugins" (Gusto 급여, Docusign 서명 등)
      보내기·결제·서명·삭제 전 승인 / 미국 Pro·Max·Ultra 대기자 명단
  - 제미나이 스파크: blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/ (2026-05-19)
      ★ 2026-11-02 사내 검토 지적으로 최신화: 발표 글만 보고 쓴 내용이 낡았음
      - 모델: Gemini 3.7 Flash (x.com/GeminiApp "Gemini Spark now runs on Gemini 3.7 Flash", 9to5google 2026-08-13)
      - 국내: 2026-07-30 구글코리아 발표, Google AI Pro 이상 순차 제공 (ZDNet·뉴스1 등) / 도움말 이용 조건 Pro·Ultra, 제외국에 한국 없음
      - 명칭: support.google.com/gemini/answer/17094507?hl=ko "이해하기 쉽도록 작업으로 이름을 변경했습니다"
      - 마지막 장 링크도 이 도움말로 (gemini.google/overview/agent/spark 는 일반 페이지로 넘어감)
      Gemini 3.5 + Antigravity / 노트북 닫거나 폰 잠가도 계속 / Gmail·Docs·Slides + Canva·OpenTable·Instacart MCP
      카드 명세서 숨은 구독료, 학교 메일 마감일 일일 요약 / 돈 쓰기·메일 발송 전 확인 / 미국 AI Ultra 베타
      (gemini.google/overview/agent/spark 는 이 PC에서 일반 제미나이 페이지로 넘어가 현재 이용 범위는 미확인)
  ★ 국내 출시(2026-11-02 사내 코멘트로 확인): dots 이용 가능(오픈AI코리아 '한국 주간 이용자 세계 3위', aitimes 216560) /
      듀엣 미국 한정 / Tasks 7-30 국내 출시 / 그록봇 국가 제한 문구 없음 / 뮤즈 미국 등 북미만 → 마지막 장 듀엣·뮤즈에 '국내 미출시' 태그
  - 그록봇: x.ai/news/introducing-grok-bot (2026-08-11) — 전용 클라우드 컴퓨터 24/7, API 없는 사이트도 로그인해 처리,
      작업을 지켜보고 루틴으로 저장, 봇끼리 메시지, SuperGrok·Cursor 구독자 베타, 기업은 대기자
  - 뮤즈: about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ (2026-09-08) — 미국, 앱·muse.ai·왓츠앱,
      메일·여행 예약·양식 작성·협상, 인스타 레시피 → 장보기 목록, 민감한 행동 전 확인 + Sentinel 에이전트,
      "free for most of what people need, with subscription plans" (가격은 공식 글에 없어 안 씀)
  - dots: openai.com/index/introducing-dots/ 한국어판 (2026-09-29, 일반 크롬은 403 → 창 띄운 크롬으로 읽음)
      GPT-6 Astra / 4,000개가 넘는 앱 / ChatGPT·Slack·Teams / 제안서 업데이트 예시 / 허용·승인·차단 맞춤 규칙,
      비밀번호 변경은 직접 / Pro·Business Premium·Enterprise, 첫 dot 추가 비용 없음
미디어(전부 공식):
  - 표지_로고.webp: 공식 아이콘 — dot 캐릭터 '펠리페'(openai.com 소개글 이미지 introducing-dots-carousel-launch 에서 잘라냄 — dots-o.svg 회색 고리는 히어로 영상 대기 이미지라 안 씀), claude.com/static/claude-duet/app-icon.svg,
      제미나이 별(구글 og 이미지에서 잘라냄), 그록봇(x.ai og 이미지에서 잘라냄), muse.ai/images/landing/brand/muse-app-icon.svg
  - 듀엣: 앤트로픽 공식 유튜브 Fb-68zqcSVs (0~11초 아침 브리핑 / 44~60초 "You keep the final say" → Send → Jenn signed)
  - 공식_커넥터.webp: claude.com 듀엣 소개글의 커넥터 아이콘 이미지 (assets.claude.com/c3618d5c….png)
  - 그록봇: x.ai 출시 글 공식 영상(media.x.ai …cursor_bot_edit_v8….mp4) 27.3~37초 "Watch me respond to emails" → 스킬로 저장
  - 뮤즈: about.fb.com 공식 영상 Introducing-Muse_Sizzle-Video.mp4 15~50초 (학교 메일 → 장보기 목록 → 대회 신청)
  - 스파크: 구글 블로그 공식 영상 UI_Gemini_GeminiSpark_v16.mp4 전체(6.9초)
  - 공식_dots제안서.webp: openai.com dots 소개글 '요구사항 변경에 맞춰 제안서 업데이트하기' 이미지
  인스타 카드 이미지·영상(녹화본)은 쓰지 않음.
"""

VOL = 31
CATEGORY = 'AI트렌드'
TITLE = '에이전틱 AI 5종: dots·듀엣·Tasks·그록봇·뮤즈'
DESCRIPTION = '오픈AI dots, 앤트로픽 클로드 듀엣, 구글 제미나이 Tasks, xAI 그록봇, 메타 뮤즈. 다섯 회사의 에이전틱 AI가 무엇을 할 수 있는지 공식 발표 기준으로 정리했습니다.'

# 라벤더: 듀엣 공식 영상의 연보라 배경 + 듀엣 로고의 테라코타 (짙은 보랏빛 밤 + 테라코타 / 라벤더 보조)
THEME = {
    'card_top': '#252136', 'card_mid': '#1A1728', 'card_bot': '#110F1C',
    'ink': '#F6F4FF', 'ink_rgb': '246, 244, 255',
    'line_rgb': '200, 194, 232', 'accent_rgb': '224, 122, 90',
    'accent': '#E07A5A', 'accent2': '#F4B79C', 'surface_rgb': '226, 222, 246',
    'sub_rgb': '185, 178, 232', 'sub': '#B9B2E8', 'sub_light': '#ECEAFB',
    'slot_bg': '#1C1930', 'deep': '#0D0B16',
    'nav_rgb': '120, 62, 44', 'nav': '#8E4A34', 'nav_hover': '#A8573D',
    'shadow_rgb': '8, 6, 14', 'cover_top': '#2C2740',
}

COVER = {
    # 배경 이미지 없이, 다섯 에이전트 공식 아이콘(로고_*.webp)을 로고와 제목 사이 가운데에 띄워 둥실거리게 한다
    'media': None,
    'html': '''
              <div class="float-logos" aria-hidden="true">
                <div class="fl" style="left:25%;top:22%;--d:0s;--t:3.4s"><img src="로고_dots.webp" alt=""><span>dots</span></div>
                <div class="fl" style="left:50%;top:14%;--d:.6s;--t:3.9s"><img src="로고_듀엣.webp" alt=""><span>Claude Duet</span></div>
                <div class="fl" style="left:75%;top:22%;--d:1.2s;--t:3.6s"><img src="로고_스파크.webp" alt=""><span>Gemini Tasks</span></div>
                <div class="fl" style="left:37%;top:66%;--d:.3s;--t:4.1s"><img src="로고_그록봇.webp" alt=""><span>Grok Bot</span></div>
                <div class="fl" style="left:63%;top:66%;--d:.9s;--t:3.7s"><img src="로고_뮤즈.webp" alt=""><span>Muse</span></div>
              </div>''',
    'headline': ('요즘 나온 에이전틱 AI,', '어떤 게 있을까요?'),
    'dek': 'dots · 듀엣 · Tasks · 그록봇 · 뮤즈',
    'css': '''    #hcn-card-1 .card-bg { background: radial-gradient(ellipse 80% 55% at 50% 44%, #2E2946 0%, #1A1728 60%, #110F1C 100%); }
    #hcn-card-1 .float-logos { position: absolute; left: 0; right: 0; top: 190px; height: 270px; z-index: 3; pointer-events: none; }
    #hcn-card-1 .fl { position: absolute; display: flex; flex-direction: column; align-items: center; transform: translate(-50%, 0); animation: logoFloat var(--t) ease-in-out var(--d) infinite; }
    #hcn-card-1 .fl img { width: 84px; height: 84px; border-radius: 30%; display: block; box-shadow: 0 14px 26px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.08); }
    #hcn-card-1 .fl span { margin-top: 8px; font-size: 12px; font-weight: 700; letter-spacing: -0.01em; color: rgba(246, 244, 255, 0.82); white-space: nowrap; }
    @keyframes logoFloat { 0%, 100% { transform: translate(-50%, 0) rotate(-1.5deg); } 50% { transform: translate(-50%, -10px) rotate(1.5deg); } }
    @media (prefers-reduced-motion: reduce) { #hcn-card-1 .fl { animation: none; } }''',
}

CARDS = [
    dict(media=('img', '공식_커넥터.webp', '클로드 듀엣이 연결하는 앱 아이콘들 — Gmail·Slack·Canva·HubSpot·Notion·Zapier 등'),
         label='에이전틱 AI가 연결해 쓰는 앱들 (앤트로픽 공식 이미지)',
         title='에이전틱 AI, 챗봇과 무엇이 다를까요?', sub='',
         body=[['챗봇은 질문에 답하고, <b>에이전틱 AI</b>는 맡긴 일을 직접 처리합니다.',
                '메일·일정·업무 앱에 연결해 읽고, 정리하고, 초안을 씁니다.',
                '클라우드에서 돌아가 내 PC를 꺼도 작업이 이어집니다.',
                '챙길 일이 생기면 묻기 전에 먼저 알려주기도 합니다.',
                '결제·발송 같은 중요한 작업 전에는 사람의 승인을 받습니다.',
                '오픈AI·앤트로픽·구글·xAI·메타가 모두 출시했습니다.']]),

    dict(media=('img', '공식_dots제안서.webp', '고객 요구사항 변경에 맞춰 제안서를 고치는 dots의 작업 화면'),
         label='요구사항 변경에 맞춰 제안서를 고치는 dots (오픈AI 공식 이미지)',
         title='1. 오픈AI dots, 슬랙·팀즈에서 일을 받습니다', sub='',
         body=[['<b>GPT-6 Astra</b> 기반의 에이전틱 AI입니다.',
                'ChatGPT와 Slack·Teams에서 업무를 지시할 수 있습니다.',
                '업무 중 새로운 요청이나 변경사항이 생기면 관련 결과물을 수정하고,',
                '판단이 필요한 사항은 사용자에게 보고합니다.',
                '연결 가능한 앱은 <b>4,000개 이상</b>입니다.',
                'Pro·Business Premium 요금제에서 dots를 사용할 수 있습니다.']]),

    dict(media=('video', '듀엣'), label='합격자에게 보낼 메일을 준비하고 승인을 기다리는 듀엣 (앤트로픽 공식 영상)',
         title='2. 클로드 듀엣, 매일 아침 할 일을 정리해 줍니다', sub='',
         body=[['<b>Opus 5.5</b> 기반의 별도 앱입니다.',
                '매일 아침 연결된 앱에서 챙길 일을 골라 보고합니다.',
                '연결 가능한 앱·도구는 <b>6,000개 이상</b>입니다.',
                '메일은 초안까지 쓰고, 발송은 사용자가 승인해야 합니다.',
                '현재 미국 유료 구독자 대상의 제한적인 연구 프리뷰로 운영 중이며,',
                '한국에는 아직 공식 출시되지 않았습니다.']]),

    dict(media=('video', '스파크'), label='"내일 야구 경기 간식 담당" 알림 후 Instacart에 간식을 담아 둔 제미나이 Tasks (구글 공식 영상)',
         title='3. 구글 제미나이 Tasks, 메일 속 할 일을 찾아냅니다', sub='',
         body=[['<b>Gemini 3.7 Flash</b> 기반의 에이전틱 AI입니다.',
                '카드 명세서에서 새로 생긴 구독료를 찾아냅니다.',
                '학교 메일의 마감일을 모아 하루 한 번 정리해 보냅니다.',
                '결제·메일 발송 전에는 먼저 확인을 받습니다.',
                '국내에서도 Google AI Pro·Ultra 구독자가 쓸 수 있습니다.']]),

    dict(media=('video', '그록봇'), label='"메일 답장하는 걸 보고 따라 해" — 시연을 보고 스킬로 저장하는 그록봇 (xAI 공식 영상)',
         title='4. 그록봇, 한 번 보여주면 그대로 반복합니다', sub='',
         body=[['xAI가 베타로 내놓은 에이전틱 AI입니다.',
                '반복 업무를 한 번 시연하면 저장해 두고 그대로 처리합니다.',
                '앱 연동이 안 되는 사이트도 내 계정으로 로그인해 작업합니다.',
                '여러 봇에 영업·채용 등 업무를 나눠 맡길 수 있습니다.',
                'SuperGrok·Cursor 유료 구독자가 이용할 수 있습니다.']]),

    dict(media=('video', '뮤즈'), label='학교 메일을 보고 준비물 목록을 만들고, 대회 신청서를 대신 작성하는 뮤즈 (메타 공식 영상)',
         title='5. 메타 뮤즈, 왓츠앱으로 일을 맡깁니다', sub='',
         body=[['<b>Muse Spark</b> 기반의 에이전틱 AI입니다.',
                '앱·웹은 물론 <b>왓츠앱</b> 메시지로도 일을 맡길 수 있습니다.',
                '저장한 레시피 영상을 장보기 목록으로 정리해 줍니다.',
                '결제 전 확인에 더해, 감시용 에이전트가 한 번 더 점검합니다.',
                '기본 기능은 무료이며 유료 구독이 따로 있습니다.',
                '현재 미국에서 먼저 출시됐으며, 한국에는 아직 출시되지 않았습니다.']]),

    dict(media=None, label='다섯 에이전틱 AI 한줄평과 공식 페이지',
         title='가장 자주 쓰는 AI부터 시작해 보세요', sub='',
         body=[['<a class="ag" href="https://openai.com/index/introducing-dots" target="_blank" rel="noopener"><img src="로고_dots.webp" alt=""><span><b>dots</b> Slack·Teams에서 일을 받는 업무형 에이전틱 AI<i><em class="tag ok" data-t="한국 이용 가능 · Pro·Business Premium"></em><u data-u="openai.com"></u></i></span></a>'],
               ['<a class="ag" href="https://claude.com/product/claude-duet" target="_blank" rel="noopener"><img src="로고_듀엣.webp" alt=""><span><b>클로드 듀엣</b> 매일 아침 할 일을 정리하고, 실행은 승인 후에<i><em class="tag no" data-t="한국 미출시 · 미국 Pro·Max·Ultra 신청 접수 중"></em><u data-u="claude.com"></u></i></span></a>'],
               ['<a class="ag" href="https://support.google.com/gemini/answer/17094507?hl=ko" target="_blank" rel="noopener"><img src="로고_스파크.webp" alt=""><span><b>제미나이 Tasks</b> 메일·명세서에서 챙길 일을 찾아 주는 비서<i><em class="tag ok" data-t="한국 이용 가능 · Google AI Pro·Ultra"></em><u data-u="support.google.com"></u></i></span></a>'],
               ['<a class="ag" href="https://x.ai/bot" target="_blank" rel="noopener"><img src="로고_그록봇.webp" alt=""><span><b>그록봇</b> 한 번 보여준 업무를 그대로 반복하는 봇 팀<i><em class="tag ok" data-t="한국 이용 가능 · SuperGrok·Cursor 구독"></em><u data-u="x.ai"></u></i></span></a>'],
               ['<a class="ag" href="https://muse.ai" target="_blank" rel="noopener"><img src="로고_뮤즈.webp" alt=""><span><b>뮤즈</b> 왓츠앱으로 생활 업무를 맡기는 개인 비서<i><em class="tag no" data-t="한국 미출시 · 미국 출시, 기본 무료"></em><u data-u="muse.ai"></u></i></span></a>']]),
]

EXTRA_CSS = '''    /* 마지막 장: 로고 + 한줄평 + 공식 페이지 링크 (지시 2026-11-02) */
    #hcn-card-8 .slide-media-slot { display: none; }
    #hcn-card-8 .slide-bottom-copy { align-items: stretch; padding: 8px 34px 18px; }
    #hcn-card-8 .slide-bottom-copy > span { display: block; width: 100%; }
    #hcn-card-8 .slide-bottom-copy a.ag { display: flex; width: 100%; box-sizing: border-box; margin: 0; border-bottom: 1px solid rgba(200, 194, 232, 0.14); font-weight: 500; color: var(--ink-dim); }
    #hcn-card-8 .slide-bottom-copy .p { display: block; margin: 0 0 12px; }
    #hcn-card-8 .ag { display: flex; align-items: center; gap: 14px; padding: 10px 12px; border-radius: 14px; text-decoration: none; color: inherit; background: rgba(226, 222, 246, 0.06); border: 1px solid rgba(200, 194, 232, 0.14); }
    #hcn-card-8 .ag:hover { background: rgba(226, 222, 246, 0.12); }
    #hcn-card-8 .ag img { width: 48px; height: 48px; border-radius: 30%; flex: none; }
    #hcn-card-8 .ag span { display: block; line-height: 1.45; }
    #hcn-card-8 .slide-bottom-copy { font-size: 15px; line-height: 1.5; }
    #hcn-card-8 .ag i { display: flex; align-items: center; gap: 8px; margin-top: 4px; font-style: normal; }
    #hcn-card-8 .ag .tag { display: inline-block; padding: 1px 8px; border-radius: 999px; font-style: normal; font-size: 11px; font-weight: 700; line-height: 1.6; white-space: nowrap; }
    #hcn-card-8 .ag .tag::before { content: attr(data-t); }
    #hcn-card-8 .ag .tag.ok { color: #0F2A1E; background: #9ED9B8; }
    #hcn-card-8 .ag .tag.no { color: #2A120B; background: #F4B79C; }
    #hcn-card-8 .ag u { text-decoration: none; font-size: 11.5px; color: rgba(185, 178, 232, 0.9); white-space: nowrap; }
    #hcn-card-8 .ag u::before { content: attr(data-u) " ↗"; }
    #hcn-card-8 .ag span b { color: #F4B79C; }'''

GABJI = {
    'bg': 'cover31.webp',
    'bg_note': '표지 로고 이미지(표지_로고.webp)를 33:25로 크롭 → cover31.webp',
    'scrim': (0.44, 0.50, 0.66),
}
