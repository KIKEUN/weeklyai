# -*- coding: utf-8 -*-
"""인스타 게시물(캐러셀) → 장별 원본 미디어 + 캡션 (가이드 §13).

사용: python fetch_insta.py https://www.instagram.com/p/<코드>/ volN/원본
      python fetch_insta.py --login      ← 처음 한 번: 창이 뜨면 인스타 로그인 후 창을 닫는다
결과: 원본/s01.mp4|jpg, s02…  +  원본/insta.json (캡션·계정·장별 종류/크기)

2026-10-20 확인: 로그아웃 상태 헤드리스는 로그인 벽만 받는다(미디어 데이터 0, 임베드도 막힘).
→ 전용 프로필(~/.weeklyai_chrome)에 한 번 로그인해 두고, 이후엔 그 프로필로 헤드리스 실행.
페이지 outerHTML 의 <script type="application/json"> 안 carousel_media 를 찾는다.
로그인이 없어도 캡션(og:description)은 받아 온다 → 컨셉 파악은 가능, 미디어는 공식 자료로(§14).
다운로드는 curl --ssl-no-revoke (사내망 인증서).
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Chrome

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PROFILE = os.path.join(os.path.expanduser('~'), '.weeklyai_chrome')
if sys.argv[1] == '--login':
    c = Chrome(1100, 900, profile=PROFILE, headless=False, start='https://www.instagram.com/accounts/login/')
    print('열린 크롬 창에서 인스타그램에 로그인한 뒤 창을 닫으세요.')
    c.proc.wait()
    print('로그인 정보 저장됨:', PROFILE)
    sys.exit(0)

url, out = sys.argv[1], sys.argv[2]
code = re.search(r'/(?:p|reel|reels)/([A-Za-z0-9_-]+)', url).group(1)
os.makedirs(out, exist_ok=True)

c = Chrome(1280, 1000, profile=PROFILE if os.path.isdir(PROFILE) else None)
try:
    c.goto('https://www.instagram.com/p/%s/' % code, 9)
    html = c.js('document.documentElement.outerHTML')
    meta_caption = c.js("(document.querySelector('meta[property=\"og:description\"]')||{}).content||''")
finally:
    c.close()
open(os.path.join(out, 'insta_page.html'), 'w', encoding='utf-8').write(html)

post = None


def walk(o):
    global post
    if post:
        return
    if isinstance(o, dict):
        if o.get('code') == code and ('carousel_media' in o or 'video_versions' in o or 'image_versions2' in o):
            post = o
            return
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


for blob in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.S):
    if code not in blob:
        continue
    try:
        walk(json.loads(blob))
    except Exception:
        pass
    if post:
        break

if not post:
    print('!! 게시물 미디어를 못 찾았습니다 (로그인 벽 / 구조 변경). insta_page.html 저장해 둠.')
    print('   → 로그인: python fetch_insta.py --login  (사용자가 직접, 1회)')
    print('   → 아니면 캡션으로 컨셉만 잡고 미디어는 공식 자료로 (§14)')
    json.dump({'url': url, 'code': code, 'caption': meta_caption, 'items': []},
              open(os.path.join(out, 'insta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n캡션(og):', meta_caption)
    sys.exit(1)

items = post.get('carousel_media') or [post]
cap = ((post.get('caption') or {}).get('text')) or meta_caption
info = {'url': url, 'code': code, 'user': (post.get('user') or {}).get('username'), 'caption': cap, 'items': []}
for i, m in enumerate(items, 1):
    if m.get('video_versions'):
        v = max(m['video_versions'], key=lambda x: x.get('width', 0) * x.get('height', 0))
        src, ext, kind = v['url'], 'mp4', 'video'
    else:
        cands = m['image_versions2']['candidates']
        v = max(cands, key=lambda x: x.get('width', 0) * x.get('height', 0))
        src, ext, kind = v['url'], 'jpg', 'image'
    fn = os.path.join(out, 's%02d.%s' % (i, ext))
    subprocess.run(['curl', '--ssl-no-revoke', '-sL', '-o', fn, src], check=True)
    ai = 'AI' in json.dumps(m.get('media_notes') or m.get('gen_ai_detection_method') or '', ensure_ascii=False)
    info['items'].append({'i': i, 'file': os.path.basename(fn), 'kind': kind, 'w': v.get('width'), 'h': v.get('height'),
                          'kb': os.path.getsize(fn) // 1024, 'ai_label': ai})
    print('s%02d %-5s %sx%s %6dKB%s' % (i, kind, v.get('width'), v.get('height'), os.path.getsize(fn) // 1024, '  [AI 표시]' if ai else ''))
json.dump(info, open(os.path.join(out, 'insta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n@%s — 캡션:\n%s' % (info['user'], cap))
