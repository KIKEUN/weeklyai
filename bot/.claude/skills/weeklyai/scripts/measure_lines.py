# -*- coding: utf-8 -*-
"""본문 줄이 실제 브라우저 폭(472px, 16.5px Pretendard)에서 넘치는지 잰다 — 이미지·영상은 띄우지 않고 글자만.

사용: python measure_lines.py 34
  각 장 본문 줄의 실제 px 폭과, 브라우저가 다시 줄바꿈한 줄(넘침)을 출력. 넘침이 있으면 exit 1.
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Chrome
from wai import load_spec, read, utf8_stdout, vol_dir

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
S = load_spec(D)
h = read(os.path.join(D, 'weeklyaivol%d_src.html' % S.VOL))
css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
font = re.search(r'<link[^>]+pretendard[^>]+>', h, re.I)
copies = re.findall(r'<div class="slide-bottom-copy">(.*?)</div>', h, re.S)
page = ('<!doctype html><meta charset="utf-8">%s<style>%s</style><body style="margin:0">' % (font.group(0) if font else '', css) +
        ''.join('<div class="card" style="position:relative!important;opacity:1;visibility:visible;display:block;height:auto">'
                '<div class="slide-bottom-copy" id="c%d" style="height:auto;overflow:visible">%s</div></div>' % (i, c)
                for i, c in enumerate(copies)) + '</body>')
tmp = os.path.join(D, '_measure.html')
open(tmp, 'w', encoding='utf-8').write(page)
c = Chrome(800, 3000)
try:
    c.goto('file:///' + tmp.replace('\\', '/'), 4)
    time.sleep(1.5)
    res = c.js(r'''JSON.stringify([...document.querySelectorAll('.slide-bottom-copy')].map(el => {
        const box = el.getBoundingClientRect(), cs = getComputedStyle(el);
        const inner = box.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        const out = [];
        el.querySelectorAll('span.p').forEach(sp => {
          const parts = sp.innerHTML.split(/<br\s*\/?>/);
          parts.forEach(p => {
            const t = document.createElement('span'); t.innerHTML = p; t.style.whiteSpace = 'nowrap';
            el.appendChild(t); out.push([t.textContent, Math.round(t.getBoundingClientRect().width)]); t.remove();
          });
        });
        return {inner: Math.round(inner), lines: out};
    }))''')
finally:
    c.close()
    os.remove(tmp)
bad = 0
for k, card in enumerate(json.loads(res), 2):
    print('%dp (폭 %dpx)' % (k, card['inner']))
    for t, w in card['lines']:
        over = w > card['inner']
        bad += over
        print('  %s %3dpx %s' % ('!!' if over else '  ', w, t))
print('넘침 %d줄' % bad if bad else '넘침 없음')
sys.exit(1 if bad else 0)
