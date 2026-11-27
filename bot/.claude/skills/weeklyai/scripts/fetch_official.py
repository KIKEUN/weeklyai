# -*- coding: utf-8 -*-
"""공식 페이지에서 영상·이미지 원본 찾기/받기 (가이드 §14).

  python fetch_official.py scan <URL>               ← 페이지 안 영상·유튜브·큰 이미지 목록
  python fetch_official.py get  <미디어URL> 저장경로   ← curl --ssl-no-revoke 로 받기
  python fetch_official.py yt   <유튜브ID|URL> 저장.mp4 ← yt-dlp (이 환경은 360p 까지)

- claude.com 제품 페이지: 화면엔 비디오가 없어도 RSC 데이터에 "videoUrl":"https://assets.claude.com/<해시>.mp4" (1080p 원본)
- 발표 글: youtube-nocookie.com/embed/<id> 만 있음 → yt 명령
- 표·차트가 HTML/SVG 이면 capture.py 로 화면 캡처
"""
import html as H, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

cmd = sys.argv[1]
if cmd == 'scan':
    url = sys.argv[2]
    page = subprocess.run(['curl', '--ssl-no-revoke', '-sL', '-A', 'Mozilla/5.0', url], capture_output=True).stdout.decode('utf-8', 'replace')
    rendered = ''
    if len(page) < 20000 or '<video' not in page:
        from cdp import Chrome
        c = Chrome()
        try:
            c.goto(url, 8)
            rendered = c.js('document.documentElement.outerHTML') or ''
        finally:
            c.close()
    blob = H.unescape((page + rendered).replace('\\/', '/').replace('\\u002F', '/'))
    vids = sorted(set(re.findall(r'https?://[^\s"\'<>()]+?\.(?:mp4|webm|m3u8)', blob)))
    yts = sorted(set(re.findall(r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_-]{11})', blob)))
    yts += sorted(set(re.findall(r'"youtubeId"\s*:\s*"([A-Za-z0-9_-]{11})"', blob)) - set(yts))
    imgs = sorted(set(re.findall(r'https?://[^\s"\'<>()]+?\.(?:webp|png|jpe?g|gif)', blob)))
    title = re.search(r'<title>(.*?)</title>', blob, re.S)
    print('제목:', title.group(1).strip() if title else '-')
    print('\n[영상 %d]' % len(vids)); [print('  ', v) for v in vids]
    print('\n[유튜브 %d]' % len(yts)); [print('   https://youtu.be/' + y) for y in yts]
    print('\n[이미지 %d] (아이콘·로고 제외하고 큰 것만 골라 쓸 것)' % len(imgs))
    for v in imgs[:60]:
        if not re.search(r'favicon|logo|icon|avatar|sprite', v, re.I):
            print('  ', v)
elif cmd == 'get':
    src, dst = sys.argv[2], sys.argv[3]
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    subprocess.run(['curl', '--ssl-no-revoke', '-sL', '-A', 'Mozilla/5.0', '-o', dst, src], check=True)
    print('받음: %s %dKB' % (dst, os.path.getsize(dst) // 1024))
elif cmd == 'yt':
    vid, dst = sys.argv[2], sys.argv[3]
    if len(vid) == 11:
        vid = 'https://www.youtube.com/watch?v=' + vid
    r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--no-playlist', '--js-runtimes', 'node', '--remote-components', 'ejs:github',
                        '--extractor-args', 'youtube:player_client=web_safari,android,ios', '--no-check-certificates',
                        '-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/18', '--merge-output-format', 'mp4', '-o', dst, vid])
    if r.returncode or not os.path.exists(dst):
        sys.exit('yt-dlp 실패 → pip install -U yt-dlp --trusted-host pypi.org --trusted-host files.pythonhosted.org 후 재시도 (§12)')
    print('받음: %s %dKB' % (dst, os.path.getsize(dst) // 1024))
else:
    sys.exit(__doc__)
