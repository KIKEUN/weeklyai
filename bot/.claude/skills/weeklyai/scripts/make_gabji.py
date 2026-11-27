# -*- coding: utf-8 -*-
"""volN/cards.py → volN/weeklyai_갑지_volN_src.html (가로 1274×971 표지 1장).

사용: python make_gabji.py 29
배지·헤드라인·dek 는 cards.py 의 COVER 를 그대로 쓰고, 색은 THEME 에서 가져온다.
배경은 GABJI['bg'] (33:25 webp). 없으면 테마 그라데이션. 배경 자르기는 media.py cover.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import TPL, load_spec, read, theme_of, utf8_stdout, vol_dir, write

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
S = load_spec(D)
theme, theme_name = theme_of(S)
G = getattr(S, 'GABJI', {}) or {}
bg = G.get('bg')
if bg and not os.path.exists(os.path.join(D, bg)):
    print('!! 배경 파일이 없습니다:', bg, '→ 그라데이션으로 만듭니다')
    bg = None
st, sm, sb = G.get('scrim', (0.44, 0.50, 0.66))
l1, l2 = S.COVER['headline']
dek = S.COVER.get('dek')

vals = dict(theme)
vals.update({
    'VOL': str(S.VOL), 'CATEGORY': S.CATEGORY, 'THEME_NAME': theme_name.split(' (')[0],
    'BG_NOTE': G.get('bg_note', bg or '테마 그라데이션'),
    'BG_IMG': '<div class="cover__bg"><img id="bgImg" src="%s" alt="" /></div>' % bg if bg else '',
    'SCRIM_TOP': '%.2f' % st, 'SCRIM_MID': '%.2f' % sm, 'SCRIM_BOT': '%.2f' % sb,
    'HEADLINE': ('%s<br />%s' % (l1, l2)).replace('<em>', '<span class="mark">').replace('</em>', '</span>')
                if '<em>' in l1 + l2 else '%s<br /><span class="mark">%s</span>' % (l1, l2),
    'DEK': '<p class="dek">%s</p>' % dek if dek else '',
})
g = read(os.path.join(TPL, 'gabji.html'))
g = re.sub(r'\{\{(\w+)\}\}', lambda m: vals[m.group(1)], g)
OUT = os.path.join(D, 'weeklyai_갑지_vol%d_src.html' % S.VOL)
write(OUT, g)
print('작성:', OUT, '| 배경:', bg or '그라데이션')
