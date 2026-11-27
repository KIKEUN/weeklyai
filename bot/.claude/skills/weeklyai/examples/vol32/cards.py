# -*- coding: utf-8 -*-
"""Weekly AI VOL.32 사양 — 이 파일 하나로 카드뉴스·갑지가 나온다 (봇 §15).
  python .claude/skills/weeklyai/scripts/make_vol.py 32 && python .claude/skills/weeklyai/scripts/check_vol.py 32
  python .claude/skills/weeklyai/scripts/make_gabji.py 32 && python .claude/skills/weeklyai/scripts/build_vol.py 32

컨셉(지시 2026-11-09): Power BI 소개 → 취소("무료버전은 안 돼서 못 쓰겠다"). '요즘 핫한 앱 5개, 한 페이지에 하나씩'.
  2p 소개 → 마지막 장으로 이동, 맺음말 '혼자 AI로 만들었다, 여러분도 만들 수 있다'. 말투는 AI스럽지 않게 자연스럽게.
  1인·AI 개발: 산사(취준생, 바이브 코딩) / 그늘로(maily.so tipster 2026-09-08 '개인 개발자', AI 활용) /
    Pieceful(요즘IT 2026-09-30 '1인 개발자', '바이브 코딩으로 만든 육아 기록 앱', 전직 외과 의사). 피클(팀)·마이모리(스타트업)는 아님 → '다섯 중 셋'
  순서(지시): 산사 먼저 → 피클 → 마이모리 → Pieceful → 그늘로. "영상이 있으면 영상으로", 공식 소개 위주.
본문 근거 (2026-11-09 확인):
  - 산사: sansatemple.com ("말없이 같이 앉아 있는 온라인 절", 염주·절하기·목탁·합장, 채팅 없음)
      연합뉴스(네이트 20261031n07418) "방구석 누워 108배로 힐링…사흘간 60만명 다녀간 온라인 산사"
      TJB "취준생이 만든 '온라인 산사'" (유튜브 8LeHWgApCP4) / 서플·나무위키: 바이브 코딩, 설치·가입 없음
      (방문자 수는 매체마다 60만·80만·130만·150만으로 다름 → 연합뉴스 60만(사흘) 사용)
  - 피클: 앱스토어 공식 설명(id6795790129, Pickle, Inc., 무료, 1.1.17 2026-10-29) — 전화 대신 걸기·주문·예약·친구 피클과 약속·승인
      디지털데일리 2026-11-03 "생산성 무료 차트 3위"(3일 기준) / 매일 기본 사용량, 새벽 4시 초기화
      인스타 ai_freaks.kr/p/DfCCtQqmk2m (CTA·초대권 추첨 장은 버림)
  - 마이모리: 앱스토어 공식 설명(id6503250569, Nuttycode, 2024-07-11 출시) — 나무가 쓰는 일기와 답장, 마음새, 암호화·Face ID
      인공지능신문·머니투데이 2026-04-22 "누적 다운로드 50만 건" / 인스타 ai_freaks.kr/p/DfHRdJXGoP_ "일본 앱스토어 건강 부문 1위"
  - Pieceful: 앱스토어 공식 설명(id6756474655, SOLMATTER, ₩7,700, 3.1.0 2026-11-03) — 사진·음성·텍스트, 기기 안 음성→글,
      주제·제목·요약 제안(Apple Intelligence, iPhone 15 Pro 이상·iOS 26), "기록한 내용을 AI 서비스로 보내지 않음", iCloud, 구독 없음
  - 그늘로: 앱스토어 공식 설명(id6791194669 '그늘로: 뚜벅의 여름길', Minjun Yoo, 무료, 2026-07-18 출시)
      — 태양·건물·가로수 그늘 경로, 버스 덜 뜨거운 창가, 밤길 CCTV·비상벨, 산책·러닝 코스
      다음(뉴시스) 2026-08-11 "2주 만에 개발", 모바일인덱스 6일 앱스토어 무료 앱 1위 / 토스 앱인토스 블로그
  - 캐리어 피지: 앱스토어 공식 설명(id6762161637, Noah Iarrobino, 무료, 2026-04-19 출시, 2.1 2026-11-03)
      — 시속 110마일 가상 비둘기, 실제 GPS 거리, 0.2% 분실, ±25% 속도, 실시간 추적, 읽음 표시 없음
      The National 2026-08-27 — 워싱턴→UAE 약 3일, 개발자 말 iOS 다운로드 14만 건
      USA TODAY 2026-08-20(AOL 재게재) — AI 챗봇으로 아이디어 정리 → Claude Code 가 "a lot" 작성, 4월 초 아이디어 → 4월 18일 앱스토어
      (앱스토어 판매자 개인 이름, 팀·공동 개발 언급 없음 → 1인 개발로 분류, 지시 2026-11-09)
미디어:
  - 산사.mp4: 유튜브 NBT TV azFRBx4-eB0 (사용자 화면 녹화, 자막·캐릭터 오버레이 없음) 184~198초 — 공식 영상 없음, 지시(사람들이 올린 영상)
  - 피클.mp4: 인스타 index 2 화면 녹화(고객센터 통화 대행) 위쪽 앱 화면만 크롭 — 피클 공식 영상 없음
  - 공식_마이모리 / 공식_pieceful / 공식_그늘로.webp: 앱스토어 공식 스크린샷 3장씩 나란히 (vol32/원본/make_media.py)
  - 로고_*.webp: 앱스토어 공식 아이콘 + sansatemple.com apple-touch-icon
"""

VOL = 32
CATEGORY = 'AI트렌드'
TITLE = '소문난 앱 6: 산사·피클·마이모리·Pieceful·그늘로·캐리어 피지'
DESCRIPTION = '온라인 절 산사, AI 비서 피클, AI 일기 마이모리, 육아 기록 Pieceful, 그늘 길찾기 그늘로, 비둘기 메신저 캐리어 피지. 요즘 화제가 된 앱 여섯 개를 공식 소개 기준으로 정리했습니다.'

# 산사 저녁: 법당의 짙은 나무색 + 불상 금빛 / 나뭇잎 초록 보조
THEME = {
    'card_top': '#2A2018', 'card_mid': '#1D1610', 'card_bot': '#120E0A',
    'ink': '#FFF7EC', 'ink_rgb': '255, 247, 236',
    'line_rgb': '236, 206, 150', 'accent_rgb': '232, 176, 74',
    'accent': '#E8B04A', 'accent2': '#F6D894', 'surface_rgb': '250, 232, 196',
    'sub_rgb': '159, 209, 138', 'sub': '#9FD18A', 'sub_light': '#E8F6DE',
    'slot_bg': '#1C150F', 'deep': '#0E0A07',
    'nav_rgb': '122, 84, 24', 'nav': '#7A5418', 'nav_hover': '#94661C',
    'shadow_rgb': '10, 7, 4', 'cover_top': '#32261C',
}

COVER = {
    # 여섯 앱의 공식 아이콘을 로고와 제목 사이에 띄워 둥실거리게 한다 (VOL.31 방식)
    'media': None,
    'html': '''
              <div class="float-logos" aria-hidden="true">
                <div class="fl" style="left:25%;top:22%;--d:0s;--t:3.4s"><img src="로고_산사.webp" alt=""><span>산사</span></div>
                <div class="fl" style="left:50%;top:14%;--d:.6s;--t:3.9s"><img src="로고_피클.webp" alt=""><span>피클</span></div>
                <div class="fl" style="left:75%;top:22%;--d:1.2s;--t:3.6s"><img src="로고_마이모리.webp" alt=""><span>마이모리</span></div>
                <div class="fl" style="left:25%;top:62%;--d:.3s;--t:4.1s"><img src="로고_pieceful.webp" alt=""><span>Pieceful</span></div>
                <div class="fl" style="left:50%;top:70%;--d:.9s;--t:3.7s"><img src="로고_그늘로.webp" alt=""><span>그늘로</span></div>
                <div class="fl" style="left:75%;top:62%;--d:1.5s;--t:3.5s"><img src="로고_캐리어피지.webp" alt=""><span>캐리어 피지</span></div>
              </div>''',
    'headline': ('소문난 <em>여섯 가지 앱</em>을', '소개합니다'),
    'dek': '산사 · 피클 · 마이모리 · Pieceful · 그늘로 · 캐리어 피지',
    'css': '''    #hcn-card-1 .card-bg { background: radial-gradient(ellipse 80% 55% at 50% 44%, #3A2C1F 0%, #1D1610 60%, #120E0A 100%); }
    #hcn-card-1 .float-logos { position: absolute; left: 0; right: 0; top: 190px; height: 270px; z-index: 3; pointer-events: none; }
    #hcn-card-1 .fl { position: absolute; display: flex; flex-direction: column; align-items: center; transform: translate(-50%, 0); animation: logoFloat var(--t) ease-in-out var(--d) infinite; }
    #hcn-card-1 .fl img { width: 84px; height: 84px; border-radius: 30%; display: block; box-shadow: 0 14px 26px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.08); }
    #hcn-card-1 .fl span { margin-top: 8px; font-size: 12px; font-weight: 700; letter-spacing: -0.01em; color: rgba(255, 247, 236, 0.82); white-space: nowrap; }
    @keyframes logoFloat { 0%, 100% { transform: translate(-50%, 0) rotate(-1.5deg); } 50% { transform: translate(-50%, -10px) rotate(1.5deg); } }
    @media (prefers-reduced-motion: reduce) { #hcn-card-1 .fl { animation: none; } }''',
}

CARDS = [
    dict(media=('video', '산사'), label='동자승 아바타들이 법당에 모여 앉아 있는 산사 화면 (사용자 화면 녹화)',
         title='1. 산사, 말없이 함께 앉아 있는 온라인 절', sub='',
         body=[['설치도 가입도 없이, 주소만 열면 바로 절 마당에 들어섭니다.',                '동자승이 되어 합장도 하고, 절도 하고, 목탁도 칩니다.',
                '채팅창이 없어서 다른 사람들과 그냥 조용히 앉아 있게 됩니다.',
                '취업 준비생 한 명이 AI로 코딩해 만들었습니다.',
                '최근 사흘 동안만 <b>60만 명</b>이 다녀갔습니다.']]),

    dict(media=('video', '피클'), label='"요금제 더 저렴한 걸로 바꿔 줘" — 고객센터에 대신 전화하는 피클 (앱 화면 녹화)',
         title='2. 피클, 개인 AI 비서', sub='', aspect='900 / 650',
         body=[['말만 하면 실제로 일을 처리해 주는 <b>AI 비서</b> 앱입니다.',
                '직접 전화를 걸어 요청한 업무를 처리할 수 있습니다.',
                '주문, 식당·KTX 예약, 친구와 약속 잡기까지 맡길 수 있습니다.',
                '결제가 필요한 일은 사용자 승인 후에 진행합니다.',
                '11월 초 앱스토어 생산성 부문 무료 <b>3위</b>에 올랐습니다.']]),

    dict(media=('img', '공식_마이모리.webp', '마이모리 앱 화면 — 나무에게 말하듯 쓰기, 마음새로 답장 받기, 주간 리포트'),
         label='나무에게 맡기는 일기, 마음새, 주간 리포트 (앱스토어 공식 이미지)', aspect='1678 / 1188',
         title='3. 마이모리, 나무가 일기에 답장을 보냅니다', sub='',
         body=[['카톡 보내듯 하루를 적으면 <b>AI 나무</b>가 일기로 정리해 줍니다.',
                '다 쓰고 나면 나무가 따뜻한 답장도 남겨 줍니다.',
                '고민을 \'마음새\'에 담아 날리면',
                '다른 나라 사용자에게서 답장이 오기도 합니다.',
                '누적 다운로드는 <b>50만 건</b>을 넘었습니다.',
                '일본 앱스토어 건강 부문에서는 <b>1위</b>까지 올랐습니다.']]),

    dict(media=('img', '공식_pieceful.webp', 'Pieceful 앱 화면 — 오늘의 기록, 주제별 이야기, 제목·요약 제안'),
         label='오늘의 기록, 주제별 이야기, 기기 안 요약 제안 (앱스토어 공식 이미지)', aspect='1678 / 1188',
         title='4. Pieceful, 아이의 하루를 이야기로 만듭니다', sub='',
         body=[['개발자 한 명이 AI로 코딩해 만든 육아 앱입니다.',
                '사진 한 장, 말 한마디로 아이의 하루를 남깁니다.',
                '목소리로 남긴 기록은 글로 바꿔 줍니다.',
                '기록은 외부 AI로 보내지 않고 내 iCloud에만 저장됩니다.',
                '<b>7,700원</b>에 내려받는 유료 앱입니다.']]),

    dict(media=('img', '공식_그늘로.webp', '그늘로 앱 화면 — 그늘 우선 경로와 버스 자리, 밤길 방범시설 경로, 지하도·역사 경로'),
         label='그늘 경로·밤길·지하도 경로 (앱스토어 공식 이미지)', aspect='1684 / 1188',
         title='5. 그늘로, 그늘길에서 밤길까지 찾습니다', sub='',
         body=[['복학을 앞둔 서울대생이 혼자 AI를 활용해 만든 길찾기 앱입니다.',
                '건물과 나무의 그림자를 따져 그늘진 길로 안내합니다.',
                '버스를 타면 햇빛이 덜 드는 쪽 자리도 알려 줍니다.',
                '밤에는 CCTV·비상벨이 많은 길로 안내합니다.',
                '폭염이 한창이던 8월에는 앱스토어 무료 앱 <b>1위</b>에 올랐습니다.']]),

    dict(media=('img', '공식_캐리어피지.webp', '캐리어 피지 앱 화면 — 실제 거리를 나는 비둘기 지도, 비행 중 메시지, 도착한 메시지'),
         label='실제 거리를 나는 비둘기, 비행 중, 도착 (앱스토어 공식 이미지)', aspect='1684 / 1188',
         title='6. 캐리어 피지, 비둘기가 메시지를 전합니다', sub='',
         body=[['소프트웨어 엔지니어 한 명이 <b>Claude Code</b>로 만든 메신저입니다.',
                '<b>GPS</b>로 잰 실제 거리만큼 가상 비둘기가 날아가 메시지를 전합니다.',
                '같은 동네면 몇 초, 다른 나라면 며칠이 걸리기도 합니다.',
                '<b>0.2%</b> 확률로 비둘기가 길을 잃어 메시지가 사라집니다.',
                '읽음 표시도 없습니다. 기다리는 재미로 쓰는 메신저입니다.',
                '출시 넉 달 만에 아이폰 다운로드 <b>14만 건</b>을 넘었습니다.']]),

    dict(media=None, label='여섯 앱 한 줄 정리 — 넷은 개발자 한 명이 AI로 만든 앱',
         title='여섯 중 넷은 혼자서 AI로 만든 앱입니다', sub='',
         body=[['<span class="ag"><img src="로고_산사.webp" alt=""><span><b>산사</b> 말없이 함께 앉아 있는 온라인 절<em>1인 개발</em></span></span>'],
               ['<span class="ag"><img src="로고_피클.webp" alt=""><span><b>피클</b> 전화·예약·주문을 대신하는 AI 비서</span></span>'],
               ['<span class="ag"><img src="로고_마이모리.webp" alt=""><span><b>마이모리</b> AI 나무가 답장해 주는 일기</span></span>'],
               ['<span class="ag"><img src="로고_pieceful.webp" alt=""><span><b>Pieceful</b> 사진·목소리로 남기는 육아 기록<em>1인 개발</em></span></span>'],
               ['<span class="ag"><img src="로고_그늘로.webp" alt=""><span><b>그늘로</b> 그늘길·밤길을 골라 주는 길찾기<em>1인 개발</em></span></span>'],
               ['<span class="ag"><img src="로고_캐리어피지.webp" alt=""><span><b>캐리어 피지</b> 비둘기가 느리게 전하는 메신저<em>1인 개발</em></span></span>']]),
]

EXTRA_CSS = '''    /* 마지막 장: 미디어 칸 없이 여섯 앱 아이콘 + 한 줄 소개 + 맺음말 (지시 2026-11-09) */
    #hcn-card-8 .slide-media-slot { display: none; }
    #hcn-card-8 .slide-bottom-copy { align-items: stretch; padding: 8px 34px 18px; font-size: 15px; line-height: 1.5; }
    #hcn-card-8 .slide-bottom-copy > span { display: block; width: 100%; }
    #hcn-card-8 .slide-bottom-copy .p { display: block; margin: 0 0 8px; }
    /* 맺음말: 본문 6줄 제한 때문에 목록 아래 ::after 로 붙인다 */
    #hcn-card-8 .slide-bottom-copy::after { content: '아이디어만 있다면, 여러분도 직접 만들어 볼 수 있습니다.'; display: block; margin-top: 6px; font-weight: 700; color: var(--ink); }
    #hcn-card-8 .ag { display: flex; align-items: center; gap: 12px; padding: 6px 12px; border-radius: 14px; background: rgba(250, 232, 196, 0.06); border: 1px solid rgba(236, 206, 150, 0.14); }
    #hcn-card-8 .ag img { width: 36px; height: 36px; border-radius: 30%; flex: none; }
    #hcn-card-8 .ag > span { display: block; flex: 1; line-height: 1.45; }
    #hcn-card-8 .ag span b { color: #F6D894; margin-right: 6px; }
    #hcn-card-8 .ag em { display: inline-block; margin-left: 8px; padding: 1px 8px; border-radius: 999px; font-style: normal; font-size: 11px; font-weight: 700; line-height: 1.6; color: #1A2614; background: #9FD18A; vertical-align: 1px; white-space: nowrap; }'''

GABJI = {
    'bg': 'cover32.webp',
    'bg_note': '산사.mp4(사용자 화면 녹화) 7초 장면을 33:25로 크롭 → cover32.webp',
    'scrim': (0.44, 0.50, 0.66),
}
