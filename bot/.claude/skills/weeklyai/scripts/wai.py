# -*- coding: utf-8 -*-
"""Weekly AI 봇 공용 모듈 — 호 사양(cards.py) 읽기, 테마 치환, 경로."""
import importlib.util, io, os, re, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(SKILL, 'template')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SKILL)))   # Weekly AI 폴더

# 템플릿(card.css / gabji.html)은 VOL.28 '자두빛 밤' 색으로 박혀 있다.
# 역할 이름 → VOL.28 값. 새 테마는 같은 역할에 다른 값을 주면 한 번에 치환된다.
ROLES = [
    ('card_top', '#22121C'), ('card_mid', '#170D14'), ('card_bot', '#0D080B'),
    ('ink', '#FFF0F7'), ('ink_rgb', '255, 240, 247'),
    ('line_rgb', '232, 164, 196'), ('accent_rgb', '214, 110, 160'),
    ('accent', '#D66EA0'), ('accent2', '#F2B8D4'), ('surface_rgb', '255, 214, 234'),
    ('sub_rgb', '143, 184, 232'), ('sub', '#8FB8E8'), ('sub_light', '#E0F0FF'),
    ('slot_bg', '#1B0F17'), ('deep', '#140610'),
    ('nav_rgb', '110, 36, 78'), ('nav', '#7A1F54'), ('nav_hover', '#90165E'),
    ('shadow_rgb', '12, 6, 9'), ('cover_top', '#30162B'),
]
ROLE_NAMES = [r for r, _ in ROLES]

THEMES = {
    # VOL.28 자두빛 밤 (짙은 자두색 + 핑크 / 하늘색 보조)
    'plum': dict(ROLES),
    # VOL.27 주말 아침 (짙은 숲색 + 민트 / 라임 보조)
    'forest': dict(zip(ROLE_NAMES, [
        '#12221B', '#0D1713', '#080D0B', '#F0FFF6', '240, 255, 246', '120, 214, 168', '70, 196, 140',
        '#46C48C', '#A8EDC4', '214, 255, 232', '206, 240, 120', '#CEF078', '#F4FFE0', '#0F1B16', '#06140D',
        '36, 110, 76', '#1F7A52', '#16905C', '6, 12, 9', '#16302A'])),
    # VOL.29 밤 도로 (짙은 남색 + 호박색 전조등 / 하늘색 보조)
    'night': dict(zip(ROLE_NAMES, [
        '#111A2E', '#0B1222', '#070B16', '#F4F6FF', '244, 246, 255', '242, 196, 122', '226, 150, 58',
        '#E2963A', '#F6CF8E', '255, 234, 204', '126, 176, 236', '#7EB0EC', '#E4EFFF', '#101A2C', '#060A14',
        '122, 72, 16', '#7A4810', '#9A5A12', '7, 11, 22', '#182744'])),
}
THEME_LABELS = {'plum': '자두빛 밤 (짙은 자두색 + 핑크 / 하늘색 보조)',
                'forest': '주말 아침 (짙은 숲색 + 민트 / 라임 보조)',
                'night': '밤 도로 (짙은 남색 + 호박색 / 하늘색 보조)'}

CATEGORIES = ('AI트렌드', 'AI리터러시', 'Copilot 소식')


def vol_dir(arg):
    """'29' / 'vol29' / 경로 → 절대 경로."""
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    n = re.sub(r'\D', '', arg)
    return os.path.join(ROOT, 'vol%s' % n)


def load_spec(d):
    path = os.path.join(d, 'cards.py')
    if not os.path.exists(path):
        sys.exit('cards.py 가 없습니다: %s  (template/cards_example.py 를 복사해서 시작)' % path)
    spec = importlib.util.spec_from_file_location('cards_spec', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if m.CATEGORY not in CATEGORIES:
        sys.exit('CATEGORY 는 %s 중 하나여야 합니다 (지금: %r)' % ('/'.join(CATEGORIES), m.CATEGORY))
    return m


def theme_of(spec):
    t = getattr(spec, 'THEME', 'plum')
    if isinstance(t, str):
        return THEMES[t], getattr(spec, 'THEME_NAME', THEME_LABELS.get(t, t))
    miss = [r for r in ROLE_NAMES if r not in t]
    if miss:
        sys.exit('THEME 에 빠진 역할: %s' % ', '.join(miss))
    return t, getattr(spec, 'THEME_NAME', '사용자 테마')


def apply_theme(text, theme):
    """VOL.28 값 → 새 값으로 한 번에 치환 (연쇄 치환 방지)."""
    src = dict((v, theme[r]) for r, v in ROLES)
    pat = re.compile('|'.join(re.escape(v) for v in sorted(src, key=len, reverse=True)))
    return pat.sub(lambda m: src[m.group(0)], text)


def read(p):
    return io.open(p, encoding='utf-8').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def utf8_stdout():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
