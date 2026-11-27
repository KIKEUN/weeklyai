# -*- coding: utf-8 -*-
"""미디어 손질 (가이드 §6, §13-3, 갑지 §5). ffmpeg 는 imageio-ffmpeg 것을 쓴다.

  python media.py img    원본.png 결과.webp [--maxw 1500] [--q 82]
  python media.py video  원본.mp4 결과이름   [--ss 68 --to 78] [--crop 720:510:0:0] [--w 900] [--crf 31] [--sound]
                         → 결과이름.mp4 + 결과이름_poster.webp (카드 슬롯용, 무음. --sound 면 오디오 유지 → cards.py 에 ('sound', 이름))
  python media.py sheet  원본.mp4 시트.png   [--n 12]       ← 구간 고를 때 보는 콘택트시트(시각 표기)
  python media.py frame  원본.mp4 프레임.png --at 71.6
  python media.py cover  원본(이미지/영상) coverN.webp [--at 초] [--box x,y,w,h]
                         → 갑지 배경 1274×971 (33:25 가운데 크롭, box 를 주면 그 영역 기준)
  python media.py info   파일
"""
import argparse, json, os, re, subprocess, sys, tempfile
import imageio_ffmpeg
from PIL import Image, ImageDraw

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
FF = imageio_ffmpeg.get_ffmpeg_exe()


def run(args):
    r = subprocess.run([FF, '-y', '-loglevel', 'error'] + args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        sys.exit('ffmpeg 실패: ' + r.stderr[-800:])


def duration(path):
    r = subprocess.run([FF, '-i', path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    s = re.search(r'Stream.*Video.*?(\d{2,5})x(\d{2,5})', r.stderr)
    d = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0
    return d, (int(s.group(1)), int(s.group(2))) if s else None


def kb(p):
    return os.path.getsize(p) // 1024


def frame(src, at, out):
    run(['-ss', str(at), '-i', src, '-frames:v', '1', out])


ap = argparse.ArgumentParser()
ap.add_argument('cmd')
ap.add_argument('src')
ap.add_argument('out', nargs='?')
ap.add_argument('--maxw', type=int, default=1500)
ap.add_argument('--q', type=int, default=82)
ap.add_argument('--ss', type=float)
ap.add_argument('--to', type=float)
ap.add_argument('--crop')
ap.add_argument('--w', type=int, default=900)
ap.add_argument('--crf', type=int, default=31)
ap.add_argument('--n', type=int, default=12)
ap.add_argument('--at', type=float, default=0)
ap.add_argument('--box')
ap.add_argument('--sound', action='store_true')
ap.add_argument('--fit16', action='store_true', help='16:9 로 잘라 사진 칸을 꽉 채움 (VOL.34 고정 기준)')
ap.add_argument('--y', type=int, help='--fit16 세로 시작점(px, 크롭 뒤 기준). 없으면 가운데')
ap.add_argument('--x', type=int, help='--fit16 가로 시작점(px, 크롭 뒤 기준). 없으면 가운데')
a = ap.parse_args()

if a.cmd == 'info':
    if a.src.lower().endswith(('.mp4', '.mov', '.webm')):
        d, wh = duration(a.src)
        print('%s  %.1f초  %s  %dKB' % (a.src, d, wh, kb(a.src)))
    else:
        im = Image.open(a.src)
        print('%s  %dx%d  %dKB' % (a.src, im.width, im.height, kb(a.src)))

elif a.cmd == 'img':
    im = Image.open(a.src).convert('RGB')
    if a.fit16:   # 사진 칸(16:9)에 꽉 차게 잘라 둔다 — 칸 크기는 절대 바꾸지 않는다
        w, h = im.size
        if w * 9 > h * 16:
            nw = h * 16 // 9
            x = min(a.x, w - nw) if a.x is not None else (w - nw) // 2
            im = im.crop((x, 0, x + nw, h))
        else:
            nh = w * 9 // 16
            y = min(a.y, h - nh) if a.y is not None else (h - nh) // 2
            im = im.crop((0, y, w, y + nh))
    nw = min(a.maxw, im.width)
    im = im.resize((nw, round(im.height * nw / im.width)), Image.LANCZOS)
    im.save(a.out, 'WEBP', quality=a.q, method=6)
    print('%s → %s  %dx%d  %dKB → %dKB' % (a.src, a.out, im.width, im.height, kb(a.src), kb(a.out)))
    if abs(im.width / im.height - 16 / 9) > 0.03:
        print('   !! 16:9 아님 → --fit16 [--y N] 으로 잘라 칸을 꽉 채우세요')

elif a.cmd == 'video':
    name = re.sub(r'\.mp4$', '', a.out)
    vf = []
    if a.crop:
        vf.append('crop=' + a.crop)
    if a.fit16:   # 크롭 뒤 화면을 16:9 로 — 세로가 길면 위아래, 가로가 길면 좌우를 자른다
        w0, h0 = duration(a.src)[1]
        if a.crop:
            w0, h0 = [int(v) for v in a.crop.split(':')[:2]]
        if w0 * 9 > h0 * 16:
            nw = h0 * 16 // 9 // 2 * 2
            x = min(a.x, w0 - nw) if a.x is not None else (w0 - nw) // 2
            vf.append('crop=%d:%d:%d:0' % (nw, h0, x))
        else:
            nh = w0 * 9 // 16 // 2 * 2
            y = min(a.y, h0 - nh) if a.y is not None else (h0 - nh) // 2
            vf.append('crop=%d:%d:0:%d' % (w0, nh, y))
    vf.append('scale=%d:-2' % a.w)
    args = []
    if a.ss is not None:
        args += ['-ss', str(a.ss)]
    if a.to is not None:
        args += ['-to', str(a.to)]
    if a.sound:   # 노래가 나와야 하는 장 (가이드 §16): 소리 유지 + 앞뒤 페이드
        d0 = (a.to - (a.ss or 0)) if a.to is not None else duration(a.src)[0] - (a.ss or 0)
        aud = ['-c:a', 'aac', '-b:a', '112k', '-af', 'afade=t=in:st=0:d=0.8,afade=t=out:st=%.1f:d=0.8' % max(0, d0 - 0.8)]
    else:
        aud = ['-an']
    run(args + ['-i', a.src] + aud + ['-vf', ','.join(vf), '-c:v', 'libx264', '-preset', 'slow', '-crf', str(a.crf),
                '-movflags', '+faststart', '-pix_fmt', 'yuv420p', name + '.mp4'])
    tmp = os.path.join(tempfile.gettempdir(), 'wai_poster.png')
    frame(name + '.mp4', 0, tmp)
    Image.open(tmp).convert('RGB').save(name + '_poster.webp', 'WEBP', quality=80, method=6)
    d, wh = duration(name + '.mp4')
    print('%s.mp4  %.1f초 %s  %dKB  (+ _poster.webp)' % (name, d, wh, kb(name + '.mp4')))
    if wh and abs(wh[0] / wh[1] - 16 / 9) > 0.03:
        print('   !! 16:9 아님 → --fit16 [--y N] 으로 다시 자르세요 (사진 칸 크기는 고정, aspect 지정 금지)')
    if kb(name + '.mp4') > 8000:
        print('   !! 8MB 넘음 → 구간을 줄이거나 --crf 33~35')

elif a.cmd == 'sheet':
    d, wh = duration(a.src)
    tiles = []
    for i in range(a.n):
        t = d * (i + 0.5) / a.n
        p = os.path.join(tempfile.gettempdir(), 'wai_sheet_%d.png' % i)
        frame(a.src, t, p)
        im = Image.open(p).convert('RGB')
        im.thumbnail((360, 360))
        ImageDraw.Draw(im).rectangle([0, 0, 70, 22], fill='black')
        ImageDraw.Draw(im).text((5, 4), '%.1fs' % t, fill='white')
        tiles.append(im)
    cols = 4
    tw, th = max(t.width for t in tiles), max(t.height for t in tiles)
    sheet = Image.new('RGB', (tw * cols, th * ((len(tiles) + cols - 1) // cols)), 'white')
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
    sheet.save(a.out)
    print('시트: %s  (%.1f초, %s)' % (a.out, d, wh))

elif a.cmd == 'frame':
    frame(a.src, a.at, a.out)
    print('프레임:', a.out)

elif a.cmd == 'cover':
    src = a.src
    if src.lower().endswith(('.mp4', '.mov', '.webm')):
        src = os.path.join(tempfile.gettempdir(), 'wai_cover.png')
        frame(a.src, a.at, src)
    im = Image.open(src).convert('RGB')
    if a.box:
        x, y, w, h = [int(v) for v in a.box.split(',')]
        im = im.crop((x, y, x + w, y + h))
    W, H = im.size
    r = 1274 / 971
    if W / H > r:
        nw = round(H * r)
        im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = round(W / r)
        im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    im.resize((1274, 971), Image.LANCZOS).save(a.out, 'WEBP', quality=88, method=6)
    print('갑지 배경: %s 1274x971 %dKB' % (a.out, kb(a.out)))
else:
    sys.exit(__doc__)
