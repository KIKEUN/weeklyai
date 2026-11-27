# -*- coding: utf-8 -*-
"""volN/cards.py → volN/weeklyaivolN_src.html (편집용 마스터) 생성.

사용: python make_vol.py 29        (또는 vol29, 또는 폴더 경로)
가이드 §4 네비 8곳(라디오·표시 CSS·prev/next·도트)은 장 수에 맞춰 자동 생성된다.
"""
import re, html as H, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import TPL, apply_theme, load_spec, read, theme_of, utf8_stdout, vol_dir, write

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
S = load_spec(D)
V = S.VOL
theme, theme_name = theme_of(S)

css = read(os.path.join(TPL, 'card.css')).replace('{{THEME_NAME}}', 'vol%d = %s' % (V, theme_name))
script = read(os.path.join(TPL, 'card_script.html'))

FOOT = ('<div class="footer"><svg class="footer-logo" viewBox="0 0 100 100" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 45L28 35V80L12 90V45Z"/>'
        '<path d="M28 5 L82 32 V48 L38 70 V54 L66 40 L28 21 V5 Z"/></svg>'
        '<span class="footer-text">AI디자인랩</span></div>')
LOGO = 'https://kikeun.github.io/weeklyai/assets/ai54.png'

CARDS = S.CARDS
N = len(CARDS) + 1   # 표지 + 본문 N장. 마무리 장 없음 (가이드 §9-3)


def media_html(m):
    if not m:
        return '<span class="media-ph">이미지 영역</span>'
    if m[0] in ('video', 'sound'):
        name = m[1]
        poster = name + '_poster.webp'
        p = ' poster="%s"' % poster if os.path.exists(os.path.join(D, poster)) else ''
        snd = ' data-sound' if m[0] == 'sound' else ''
        v = ('<video autoplay muted loop playsinline preload="auto" disablepictureinpicture%s%s>'
             '<source src="%s.mp4" type="video/mp4"></video>' % (p, snd, name))
        if snd:   # 소리 나는 장 (가이드 §16): 첫 클릭 뒤 자동으로 소리 켜짐, 안 되면 이 버튼
            v += ('\n                    <button class="sound-btn" type="button" aria-pressed="false" aria-label="노래 소리 켜기/끄기">'
                  '<span class="ico" aria-hidden="true">♪</span><span class="txt">소리 켜기</span></button>')
        return v
    return '<img src="%s" alt="%s" loading="eager" decoding="async" />' % (m[1], H.escape(m[2] if len(m) > 2 else '', quote=True))


W_MAX = 37.0   # 한 줄 폭: 한글 1, 영숫자·공백 0.6 (check_vol 과 같은 셈). 실제 폭 480px 기준 — measure_lines.py 로 실측 확인


def _w(t):
    t = re.sub(r'<[^>]+>', '', t)
    return sum(1.0 if ord(c) > 0x1100 else 0.6 for c in t)


def _tail(words, i, j):
    """줄 끝 모양 벌점: 문장이 끝난 뒤 다음 문장 첫 어절 하나만 매달린 줄("~습니다. 두")을 피하고,
    마침표·쉼표에서 끊기는 줄은 조금 우대한다."""
    last = re.sub(r'<[^>]+>', '', words[j - 1])
    if j == len(words) or last.endswith('.'):
        return -30.0   # 문장 끝에서 줄을 끊는 것을 강하게 우대 (VOL.34 "4개뿐이었습니다. 줄 위로 올려")
    if last.endswith(','):
        return -4.0
    k = j - 2
    tail_words = 1
    while k >= i and not re.sub(r'<[^>]+>', '', words[k]).endswith('.'):
        k -= 1; tail_words += 1
    pen = 60.0 if k >= i and tail_words <= 3 else 0.0   # "…놓쳤습니다. 두 모델 모두" 처럼 다음 문장 첫 3어절까지 매달리면 벌점
    # 줄 첫머리가 앞 문장의 꼬리 한 어절로만 끝나는 경우("…모델은 / 4개뿐이었습니다.") — 윗줄로 올린다 (VOL.34 지시)
    first = re.sub(r'<[^>]+>', '', words[i])
    if i > 0 and first.endswith('.') and not re.sub(r'<[^>]+>', '', words[i - 1]).endswith('.'):
        pen += 60.0
    return pen


def wrap(text, wmax=W_MAX):
    """문단 문자열 → 줄 목록. 줄바꿈을 손으로 정하지 않는다 (가이드 §9-4 C-3, VOL.34 지시 "왜 줄바꿈을 니맘대로").
    어절 단위로만 끊고, 가장 적은 줄 수 안에서 줄 길이가 가장 고르게 되도록 나눈다(마지막 줄 외톨이 방지).
    <b>…</b> 는 한 어절 안에 열고 닫는다고 가정한다."""
    words = []
    for x in text.split():
        # 영문 모델명은 한 덩어리로: 한글 없는 어절 + 영숫자로 시작하는 다음 어절은 붙인다 (Solar Mini 4.5 Preview가)
        if words and not re.search(r'[가-힣]', re.sub(r'<[^>]+>', '', words[-1])) and re.match(r'(<[^>]+>)*[A-Za-z0-9]', x):
            words[-1] += ' ' + x
        else:
            words.append(x)
    n = len(words)
    sp = _w(' ')
    def seg(i, j):
        return sum(_w(x) for x in words[i:j]) + sp * (j - i - 1)
    # 최소 줄 수 (그리디)
    lines, cur = 1, 0.0
    for x in words:
        add = _w(x) if cur == 0 else sp + _w(x)
        if cur and cur + add > wmax:
            lines += 1; cur = _w(x)
        else:
            cur += add
    target = seg(0, n) / lines
    INF = float('inf')
    best = [[INF] * (lines + 1) for _ in range(n + 1)]
    prev = [[0] * (lines + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for j in range(1, n + 1):
        for k in range(1, lines + 1):
            for i in range(j - 1, -1, -1):
                w = seg(i, j)
                if w > wmax:
                    break
                c = best[i][k - 1] + (w - target) ** 2 + _tail(words, i, j)
                if c < best[j][k]:
                    best[j][k], prev[j][k] = c, i
    out, j, k = [], n, lines
    while k:
        i = prev[j][k]
        out.append(' '.join(words[i:j])); j, k = i, k - 1
    return out[::-1]


def body(paras):
    # 문단은 문자열(자동 줄바꿈, 권장) 또는 줄 목록(기존 호 호환)
    return '\n                      '.join('<span class="p">%s</span>' % '<br />'.join(wrap(p) if isinstance(p, str) else p)
                                         for p in paras)


def card(k, c):
    sub = c.get('sub') or ''
    return '''
            <section class="card" id="hcn-card-{k}" aria-label="슬라이드 {k}">
              <div class="card-bg"></div>
              <span class="card-pageno">{k} / {n}</span>
              <div class="card-content card-content--inner">
                <div class="slide-body">
                  <div class="slide-top-copy">
                    <p class="subkicker">{title}</p>
{sub}                  </div>
                  <div class="slide-media-slot{ph}" aria-label="{label}">
                    {media}
                  </div>
                  <div class="slide-bottom-copy">
                    <span>
                      {body}
                    </span>
                  </div>
                </div>
                {foot}
              </div>
            </section>
'''.format(k=k, n=N, title=c['title'], sub=('                    <p class="kicker">%s</p>\n' % sub) if sub else '',
           ph='' if c.get('media') else ' slide-media-slot--ph', label=H.escape(c.get('label', ''), quote=True),
           media=media_html(c.get('media')), body=body(c['body']), foot=FOOT)


# ── 표지 ──
C = S.COVER
cm = C.get('media')
if cm and cm[0] == 'video':
    poster = cm[1] + '_poster.webp'
    p = ' poster="%s"' % poster if os.path.exists(os.path.join(D, poster)) else ''
    cover_media = ('<video class="cover-media-img" autoplay muted loop playsinline preload="auto" disablepictureinpicture%s>'
                   '<source src="%s.mp4" type="video/mp4"></video>' % (p, cm[1]))
elif cm:
    cover_media = '<img class="cover-media-img" src="%s" alt="" loading="eager" decoding="async" />' % cm[1]
else:
    cover_media = ''
cover_media += C.get('html', '')   # 표지 위에 얹는 호별 마크업 (VOL.31 떠다니는 로고들)
l1, l2 = C['headline']
# 줄 안에 <em>…</em> 이 있으면 그 부분만 강조색, 없으면 2줄 전체 강조 (VOL.32)
if '<em>' in l1 + l2:
    l1, l2 = [l.replace('<em>', '<span class="cover-headline__mark">').replace('</em>', '</span>') for l in (l1, l2)]
    HL2_CLASS = ''
else:
    HL2_CLASS = ' class="cover-headline__mark"'
cards = ['''
            <!-- ▭▭▭ 1p 표지 ▭▭▭ -->
            <section class="card card--cover" id="hcn-card-1" aria-label="슬라이드 1 표지">
              <div class="card-bg"></div>
              {media}
              <span class="card-pageno">1 / {n}</span>
              <div class="cover-bottom-deco" aria-hidden="true"></div>
              <div class="card-content card-content--cover">
                <span class="cover-badge cover-badge--top">VOL.{v} ｜ {cat}</span>
                <div class="cover-inner">
                  <div class="cover-top">
                    <figure class="cover-figure"><img src="{logo}" alt="Weekly AI" referrerpolicy="no-referrer" loading="eager" decoding="async"></figure>
                  </div>
                  <div class="cover-hero-wrap">
                    <div class="cover-hero">
                      <h1 class="cover-headline">
                        <strong>{l1}</strong><br />
                        <strong{hl2}>{l2}</strong>
                      </h1>
{dek}                    </div>
                  </div>
                </div>
                {foot}
              </div>
            </section>
'''.format(media=cover_media, n=N, v=V, cat=S.CATEGORY, logo=LOGO, l1=l1, l2=l2, hl2=HL2_CLASS,
           dek=('                      <p class="cover-dek">%s</p>\n' % C['dek']) if C.get('dek') else '', foot=FOOT)]

for k, c in enumerate(CARDS, start=2):
    cards.append(card(k, c))

# ── 호별 CSS: 표지 배치 + 장별 슬롯 비율 + 자유 CSS ──
extra = ['', '    /* ════════ vol%d 추가 ════════ */' % V]
if C.get('css'):
    extra.append(C['css'].rstrip())
for k, c in enumerate(CARDS, start=2):
    if c.get('aspect'):
        extra.append('    #hcn-card-%d .slide-media-slot { aspect-ratio: %s; }' % (k, c['aspect']))
if getattr(S, 'EXTRA_CSS', ''):
    extra.append(S.EXTRA_CSS.rstrip())
css = css.rstrip() + '\n' + '\n'.join(extra) + '\n'
css = apply_theme(css, theme)

# ── 네비게이션 (가이드 §4의 8곳) ──
radios = '\n'.join('    <input class="wai-nav" type="radio" name="hcn-nav" id="hcn-nav-%d" autocomplete="off"%s>'
                   % (k, ' checked' if k == 1 else '') for k in range(1, N + 1))
vis = ',\n'.join('    #hcn-nav-%d:checked ~ .carousel-row #hcn-card-%d' % (k, k) for k in range(1, N + 1))
prev_css = '\n'.join('    #hcn-nav-%d:checked ~ .carousel-row .nav-prev-from-%d { display: inline-flex; }' % (k, k) for k in range(2, N + 1))
next_css = '\n'.join('    #hcn-nav-%d:checked ~ .carousel-row .nav-next-from-%d { display: inline-flex; }' % (k, k) for k in range(1, N))
dot_css = ',\n'.join('    #hcn-nav-%d:checked ~ .progress-dots .dot:nth-child(%d)' % (k, k) for k in range(1, N + 1))

css = re.sub(r'(    #hcn-nav-\d+:checked ~ \.carousel-row #hcn-card-\d+,\n)*    #hcn-nav-\d+:checked ~ \.carousel-row #hcn-card-\d+ \{', lambda m: vis + ' {', css, count=1)
css = re.sub(r'(    #hcn-nav-\d+:checked ~ \.carousel-row \.nav-prev-from-\d+ \{ display: inline-flex; \}\n)+', lambda m: prev_css + '\n', css, count=1)
css = re.sub(r'#hcn-nav-\d+:checked ~ \.carousel-row \.nav-prev-disabled', '#hcn-nav-1:checked ~ .carousel-row .nav-prev-disabled', css)
css = re.sub(r'(    #hcn-nav-\d+:checked ~ \.carousel-row \.nav-next-from-\d+ \{ display: inline-flex; \}\n)+', lambda m: next_css + '\n', css, count=1)
css = re.sub(r'#hcn-nav-\d+:checked ~ \.carousel-row \.nav-next-disabled', '#hcn-nav-%d:checked ~ .carousel-row .nav-next-disabled' % N, css)
css = re.sub(r'(    #hcn-nav-\d+:checked ~ \.progress-dots \.dot:nth-child\(\d+\),\n)*    #hcn-nav-\d+:checked ~ \.progress-dots \.dot:nth-child\(\d+\) \{', lambda m: dot_css + ' {', css, count=1)

prev_html = '\n'.join(['        <span class="nav-btn nav-btn--prev nav-prev-disabled is-disabled" aria-hidden="true">←</span>'] +
                      ['        <label class="nav-btn nav-btn--prev nav-prev-from-%d" for="hcn-nav-%d" aria-label="이전 슬라이드">←</label>' % (k, k - 1) for k in range(2, N + 1)])
next_html = '\n'.join(['        <label class="nav-btn nav-btn--next nav-next-from-%d" for="hcn-nav-%d" aria-label="다음 슬라이드">→</label>' % (k, k + 1) for k in range(1, N)] +
                      ['        <span class="nav-btn nav-btn--next nav-next-disabled is-disabled" aria-hidden="true">→</span>'])
dots = '<span class="dot"></span>' * N

title = H.escape(S.TITLE)
desc = H.escape(getattr(S, 'DESCRIPTION', ''), quote=True)
page = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <title>Weekly AI VOL.{v} — {title}</title>
  <meta name="description" content="{desc}" />
  <meta property="og:title" content="Weekly AI VOL.{v} — {title}" />
  <meta property="og:description" content="{dek}. AI디자인랩 주간 카드뉴스" />
  <meta property="og:type" content="article" />
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@latest/dist/web/static/pretendard.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <div class="carousel-shell" id="html-cardnews-vol{v}">
{radios}

    <div class="carousel-row">
      <div class="nav-stack nav-stack--prev">
{prev}
      </div>

      <div class="carousel__viewport">
        <div class="carousel__inner">
          <div id="deck">{cards}
          </div>
        </div>
      </div>

      <div class="nav-stack nav-stack--next">
{next}
      </div>
    </div>

    <div class="progress-dots" aria-hidden="true">
      {dots}
    </div>
  </div>

  <div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-label="미디어 확대 보기">
    <button class="lightbox-close" type="button" aria-label="닫기">&times;</button>
    <img id="lightbox-img" src="" alt="" />
    <video id="lightbox-video" muted loop playsinline controls style="display:none"></video>
  </div>

  {script}
</body>
</html>
'''.format(v=V, title=title, desc=desc, dek=H.escape(re.sub(r'<[^>]+>', '', C.get('dek', '')), quote=True),
           css=css, radios=radios, prev=prev_html, cards=''.join(cards), next=next_html, dots=dots, script=script)

OUT = os.path.join(D, 'weeklyaivol%d_src.html' % V)
write(OUT, page)
print('작성:', OUT, '%dKB, %d장 (표지 + %d)' % (len(page) // 1024, N, len(CARDS)))
