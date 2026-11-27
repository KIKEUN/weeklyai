# -*- coding: utf-8 -*-
"""공식 페이지의 표·차트·카드를 화면 그대로 캡처 (가이드 §12, §14-3).

사용: python capture.py <URL> "<CSS 선택자>" <저장.webp> [--index 0] [--width 1440] [--pad 0]
      python capture.py <URL> --list "table, svg, figure, img"   ← 후보 요소 목록만 출력

clip 좌표는 쓰지 않는다: scrollIntoView → 뷰포트 전체 캡처 → getBoundingClientRect×DPR 로 PIL 크롭.
강제 표시 CSS(opacity:1!important)는 넣지 않는다(숨은 오버레이가 덮음). 쿠키 배너만 지운다.
"""
import argparse, json, os, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Chrome
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ap = argparse.ArgumentParser()
ap.add_argument('url')
ap.add_argument('selector', nargs='?')
ap.add_argument('out', nargs='?')
ap.add_argument('--index', type=int, default=0)
ap.add_argument('--width', type=int, default=1440)
ap.add_argument('--height', type=int, default=1000)
ap.add_argument('--pad', type=int, default=0, help='요소 둘레 여백(px)')
ap.add_argument('--list', help='후보 요소 선택자 — 목록만 출력')
ap.add_argument('--maxw', type=int, default=1500)
a = ap.parse_args()

KILL = "document.querySelectorAll('[class*=cookie],[id*=cookie],[id*=onetrust],[class*=consent]').forEach(e=>e.remove())"

c = Chrome(a.width, a.height)
try:
    c.goto(a.url, 8)
    c.js(KILL)
    # 지연 로딩 요소를 깨우려고 끝까지 한 번 내렸다 올린다
    c.js("(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}scrollTo(0,0);})()")
    time.sleep(2)
    if a.list:
        rows = c.js("""[...document.querySelectorAll(%s)].map((e,i)=>{const r=e.getBoundingClientRect();
            return [i,e.tagName,Math.round(r.width),Math.round(r.height),(e.innerText||e.getAttribute('alt')||e.getAttribute('src')||'').replace(/\\s+/g,' ').slice(0,70)]}).filter(x=>x[2]>200&&x[3]>120)""" % json.dumps(a.list))
        for r in rows or []:
            print('%3d %-7s %4dx%-4d %s' % tuple(r))
        sys.exit(0)
    sel = json.dumps(a.selector)
    n = c.js('document.querySelectorAll(%s).length' % sel)
    if not n:
        sys.exit('선택자에 맞는 요소가 없습니다: %s' % a.selector)
    c.js("document.querySelectorAll(%s)[%d].scrollIntoView({block:'center'})" % (sel, a.index))
    time.sleep(2.5)
    c.js(KILL)
    r = c.js("(()=>{const r=document.querySelectorAll(%s)[%d].getBoundingClientRect();return [r.left,r.top,r.width,r.height,devicePixelRatio]})()" % (sel, a.index))
    tmp = os.path.join(tempfile.gettempdir(), 'wai_cap.png')
    c.shot(tmp)
finally:
    c.close()

x, y, w, h, dpr = r
p = a.pad
im = Image.open(tmp).convert('RGB')
box = [max(0, int((x - p) * dpr)), max(0, int((y - p) * dpr)),
       min(im.width, int((x + w + p) * dpr)), min(im.height, int((y + h + p) * dpr))]
if h > a.height:
    print('!! 요소가 뷰포트(%dpx)보다 깁니다(%dpx) → --height 를 키우세요' % (a.height, h))
crop = im.crop(box)
if crop.width > a.maxw:
    crop = crop.resize((a.maxw, round(crop.height * a.maxw / crop.width)), Image.LANCZOS)
crop.save(a.out, 'WEBP', quality=88, method=6)
print('저장: %s  %dx%d' % (a.out, crop.width, crop.height))
if abs(crop.width / crop.height - 16 / 9) > 0.03:
    print('   !! 16:9 아님 → media.py img --fit16 [--y N] 으로 잘라 칸을 꽉 채우기 (aspect 지정 금지, 가이드 §9-4)')
