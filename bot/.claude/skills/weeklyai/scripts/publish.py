# -*- coding: utf-8 -*-
"""배포본 weeklyaivolN.html 1개를 KIKEUN/weeklyai 루트에 올린다 (gh api, 커밋은 KIKEUN 명의).

사용: python publish.py 29            ← "올려줘" 지시가 있을 때만 실행
갑지 HTML·원본 미디어는 올리지 않는다. 올린 뒤 git hash-object --no-filters 로 원격 sha 대조.
"""
import base64, json, os, re, subprocess, sys, tempfile, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import utf8_stdout, vol_dir

utf8_stdout()
REPO = 'KIKEUN/weeklyai'
D = vol_dir(sys.argv[1])
n = re.sub(r'\D', '', os.path.basename(D))
name = 'weeklyaivol%s.html' % n
path = os.path.join(D, name)
html = open(path, encoding='utf-8').read()
if re.search(r'\b(?:src|poster)="(?!https?:|data:)[^"]+"', html):
    sys.exit('중단: 로컬 파일 참조가 남아 있습니다. build_vol.py 를 먼저 돌리세요.')

api = 'repos/%s/contents/%s' % (REPO, urllib.parse.quote(name))
old = subprocess.run(['gh', 'api', api, '--jq', '.sha'], capture_output=True, text=True)
sha = old.stdout.strip() if old.returncode == 0 else None
payload = {'message': ('Update ' if sha else 'Add ') + name, 'content': base64.b64encode(open(path, 'rb').read()).decode()}
if sha:
    payload['sha'] = sha
tmp = os.path.join(tempfile.gettempdir(), 'wai_payload.json')
json.dump(payload, open(tmp, 'w'))
r = subprocess.run(['gh', 'api', '--method', 'PUT', api, '--input', tmp, '--jq', '.content.sha + " " + .commit.sha'],
                   capture_output=True, text=True)
os.remove(tmp)
if r.returncode:
    sys.exit('업로드 실패: ' + r.stderr)
remote, commit = r.stdout.split()
local = subprocess.run(['git', 'hash-object', '--no-filters', path], capture_output=True, text=True).stdout.strip()
print('%s %s  (%dKB)' % ('갱신' if sha else '신규', name, os.path.getsize(path) // 1024))
print('커밋 %s | sha 대조 %s' % (commit[:7], '일치' if local == remote else '불일치 %s ≠ %s' % (local, remote)))
print('https://kikeun.github.io/weeklyai/%s' % name)
