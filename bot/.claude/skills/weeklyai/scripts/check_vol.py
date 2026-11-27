# -*- coding: utf-8 -*-
"""검사 두 가지만 (가이드 §9-3 D): 줄 길이 + 구조. 브라우저 캡처 검증은 하지 않는다.

사용: python check_vol.py 29
"""
import html as H, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import load_spec, read, utf8_stdout, vol_dir

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
S = load_spec(D)
h = read(os.path.join(D, 'weeklyaivol%d_src.html' % S.VOL))
N = len(S.CARDS) + 1
bad = []

# 1) 줄 길이: 한글 37자(영숫자 0.6) 이내, 장당 6줄 이내
for k in range(2, N + 1):
    s = re.search(r'<section class="card" id="hcn-card-%d"(?:.|\n)*?</section>' % k, h).group(0)
    b = re.search(r'<div class="slide-bottom-copy">(?:.|\n)*?</span>\s*</div>', s).group(0)
    lines = [H.unescape(re.sub(r'<[^>]+>', '', l)).strip() for l in re.split(r'<br />|</span>', b)]
    lines = [l for l in lines if l]
    for l in lines:
        w = sum(1.0 if ord(c) > 0x1100 else 0.6 for c in l)
        if w > 37.5:   # 실제 폭 480px 기준 (VOL.34 실측). 정밀 판정은 measure_lines.py
            bad.append('%dp 줄 길이 %.0f자: %s' % (k, w, l))
    if len(lines) > 6:
        bad.append('%dp 본문 %d줄 (6줄까지)' % (k, len(lines)))
    t = re.search(r'class="subkicker">([^<]*)<', s).group(1)
    if sum(1.0 if ord(c) > 0x1100 else 0.6 for c in t) > 36:   # 25px 제목은 한 줄 약 18자, 두 줄까지 허용
        bad.append('%dp 제목이 세 줄로 넘어감: %s' % (k, t))

# 2) 구조: 네비 8곳이 N 과 맞는지
nums = lambda p: sorted(set(int(x) for x in re.findall(p, h)))
want = list(range(1, N + 1))
checks = {
    'radio': nums(r'id="hcn-nav-(\d+)"') == want,
    'card': nums(r'id="hcn-card-(\d+)"') == want,
    'prev': nums(r'nav-prev-from-(\d+)') == want[1:],
    'next': nums(r'nav-next-from-(\d+)') == want[:-1],
    'dots': h.count('<span class="dot"></span>') == N,
    'visib': len(re.findall(r'#hcn-nav-\d+:checked ~ \.carousel-row #hcn-card-\d+', h)) == N,
    'dotcss': nums(r'dot:nth-child\((\d+)\)') == want,
    'pageno': len(re.findall(r'class="card-pageno">\d+ / %d<' % N, h)) == N,
    'next-disabled': ('#hcn-nav-%d:checked ~ .carousel-row .nav-next-disabled' % N) in h,
}
for k, ok in checks.items():
    if not ok:
        bad.append('구조 불일치: ' + k)
for k in nums(r'#hcn-card-(\d+) \.slide-media-slot \{ aspect-ratio'):
    if k > N:
        bad.append('슬롯 비율 CSS 가 없는 장(%d)을 가리킴' % k)

# 2-1) 고정 레이아웃 (지시 2026-11-23): 제목·사진 칸 크기·본문 위치는 VOL.20번대 기본값 그대로.
#      장별 aspect, EXTRA_CSS 로 슬롯 비율·제목·본문 위치를 바꾸는 것 금지. 사진은 16:9 칸 안에 contain/cover 로만 맞춘다.
for i, c in enumerate(S.CARDS, 2):
    if c.get('aspect'):
        bad.append('%dp aspect 지정 금지 — 사진 칸은 16:9 고정' % i)
ex = getattr(S, 'EXTRA_CSS', '') or ''
for pat, why in [(r'aspect-ratio', '슬롯 비율'), (r'\.slide-(title|body|bottom-copy|head|kicker)|\.subkicker', '제목·본문 위치'),
                 (r'\.slide-media-slot\s*\{[^}]*(height|width|margin|padding|top|bottom)', '사진 칸 크기')]:
    if re.search(pat, ex):
        bad.append('EXTRA_CSS 가 %s 을 바꿈 — 고정값 유지' % why)

# 2-2) 사진 꽉 채우기 (VOL.34 고정 기준, 가이드 §9-4): 모든 장 미디어 파일이 16:9 — media.py --fit16 으로 자른다.
#      contain(여백 띠) 금지. 영상은 _poster.webp 크기로 본다.
from PIL import Image
for i, c in enumerate(S.CARDS, 2):
    m = c.get('media')
    if not m:
        continue
    f = os.path.join(D, m[1] + '_poster.webp') if m[0] in ('video', 'sound') else os.path.join(D, m[1])
    if os.path.exists(f):
        w, hh = Image.open(f).size
        if abs(w / hh - 16 / 9) > 0.03:
            bad.append('%dp 미디어 %dx%d 가 16:9 아님 → media.py --fit16 [--y N] 으로 다시 자르기' % (i, w, hh))
if re.search(r'object-fit\s*:\s*contain', ex):
    bad.append('EXTRA_CSS object-fit: contain 금지 — 미디어를 16:9 로 잘라 꽉 채움')

# 2-3) 문구 = 기자 브리핑 (가이드 §9-4 C): AI 같은 감상·해석형 표현, 구어 어미 금지
AI_TONE = ['보여 줍니다', '보여줍니다', '보입니다', '차이를 만듭니다', '다음 과제', '놀랍', '꽤 ', '진심으로', '응원합니다',
           '거죠', '했죠', '이죠', '네요', '답니다', '랍니다', '셈입니다', '시대입니다', '단계입니다', '수준입니다',
           '중요한 건', '핵심은', '무엇보다', '!', '?']
for i, c in enumerate(S.CARDS, 2):
    for l in (x for blk in c['body'] for x in ([blk] if isinstance(blk, str) else blk)):
        t = H.unescape(re.sub(r'<[^>]+>', '', l))
        for w in AI_TONE:
            if w in t.replace('바랍니다', ''):   # '바랍니다'는 정상 표현 — '~랍니다' 오탐 제외
                bad.append('%dp AI 같은 표현 "%s": %s' % (i, w.strip(), t))

# 3) 규칙: 링크·각주 없음, 로고 주소
if 'slide-footnote"><dl>' in h:
    bad.append('각주 블록이 있음 (§9-3 B 폐지)')
if re.search(r'<a href=', h):
    bad.append('본문 링크가 있음 (§9-3 B 폐지)')
if 'kikeun.github.io/weeklyai/assets/ai54.png' not in h:
    bad.append('표지 로고 주소가 weeklyai/assets/ai54.png 가 아님')
for m in re.findall(r'\b(?:src|poster)="([^"]+)"', h):
    if not m.startswith(('http', 'data:')) and m and not os.path.exists(os.path.join(D, m)):
        bad.append('미디어 파일 없음: ' + m)

print('VOL.%d  %d장  검사 %s' % (S.VOL, N, '통과' if not bad else '문제 %d건' % len(bad)))
for b in bad:
    print('  -', b)
sys.exit(1 if bad else 0)
