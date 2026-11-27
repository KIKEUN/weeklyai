# -*- coding: utf-8 -*-
"""배포본 빌드 (가이드 §11): 로컬 미디어를 전부 base64 로 내장한 단일 HTML.

  weeklyaivolN_src.html        → weeklyaivolN.html          (깃허브에 올리는 건 이것 하나)
  weeklyai_갑지_volN_src.html  → weeklyai_갑지_volN.html    (있으면. PNG 저장용, 저장소엔 안 올림)

사용: python build_vol.py 29
"""
import base64, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import read, utf8_stdout, vol_dir, write

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
n = re.sub(r'\D', '', os.path.basename(D))
MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.gif': 'image/gif', '.mp4': 'video/mp4', '.svg': 'image/svg+xml'}


def embed(src, out):
    html = read(src)
    missing, done = [], []

    def b64(val):
        path = os.path.join(D, val)
        if not os.path.exists(path):
            missing.append(val)
            return None
        done.append((val, os.path.getsize(path)))
        return 'data:%s;base64,%s' % (MIME.get(os.path.splitext(val)[1].lower(), 'application/octet-stream'),
                                      base64.b64encode(open(path, 'rb').read()).decode())

    def attr(m):
        val = m.group(3)
        if val.startswith(('http://', 'https://', 'data:', '#', '//')) or not val:
            return m.group(0)
        d = b64(val)
        return m.group(0) if d is None else '%s%s%s%s' % (m.group(1), m.group(2), d, m.group(2))

    def cssurl(m):
        val = m.group(1).strip().strip('\'"')
        if val.startswith(('http', 'data:', '#', '%23')):
            return m.group(0)
        d = b64(val)
        return m.group(0) if d is None else 'url("%s")' % d

    html = re.sub(r'(\b(?:src|poster)=)(["\'])([^"\']*)\2', attr, html)
    html = re.sub(r'url\((\s*[^)]+?\s*)\)', cssurl, html)
    write(out, html)
    left = [v for v in re.findall(r'\b(?:src|poster)=["\']([^"\']+)["\']', html) if not v.startswith(('http', 'data:'))]
    print('\n[%s] 내장 %d개, 배포본 %dKB' % (os.path.basename(out), len(done), os.path.getsize(out) // 1024))
    for v, s in done:
        print('   %-26s %6dKB' % (v, s // 1024))
    if missing:
        print('!! 파일 없음 (배포 시 깨짐):', sorted(set(missing)))
    print('   남은 로컬 참조:', left or '없음')
    return not missing and not left


ok = True
for src, out in [('weeklyaivol%s_src.html' % n, 'weeklyaivol%s.html' % n),
                 ('weeklyai_갑지_vol%s_src.html' % n, 'weeklyai_갑지_vol%s.html' % n)]:
    if os.path.exists(os.path.join(D, src)):
        ok &= embed(os.path.join(D, src), os.path.join(D, out))
sys.exit(0 if ok else 1)
