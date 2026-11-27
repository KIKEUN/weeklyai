# -*- coding: utf-8 -*-
"""헤드리스 크롬 최소 CDP 클라이언트 (가이드 §12 함정 반영).

- 실행마다 새 --user-data-dir + 새 포트 (같은 프로필을 잡으면 안 뜸, Stop-Process 는 정책상 막힘)
- --remote-allow-origins=* (없으면 403)
"""
import json, os, random, shutil, socket, subprocess, tempfile, time, urllib.request
import websocket

CHROME = [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
          r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe']


def _free_port():
    for _ in range(50):
        p = random.randint(9300, 9900)
        with socket.socket() as s:
            if s.connect_ex(('127.0.0.1', p)):
                return p
    raise RuntimeError('빈 포트 없음')


class Chrome:
    def __init__(self, width=1440, height=1000, mobile=False, profile=None, headless=True, start='about:blank'):
        """profile: 로그인 유지용 고정 프로필 폴더(없으면 매번 새 임시 폴더). headless=False 면 창이 뜬다."""
        exe = next(p for p in CHROME if os.path.exists(p))
        self.port = _free_port()
        self.keep = bool(profile)
        self.prof = profile or tempfile.mkdtemp(prefix='wai_cdp_')
        os.makedirs(self.prof, exist_ok=True)
        args = [exe, '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                '--hide-scrollbars', '--mute-audio', '--remote-allow-origins=*',
                '--remote-debugging-port=%d' % self.port, '--user-data-dir=' + self.prof,
                '--window-size=%d,%d' % (width, height), start]
        if headless:
            args.insert(1, '--headless=new')
        if mobile:
            args.insert(1, '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
                           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tabs = None
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % self.port, timeout=2))
                if any(t.get('type') == 'page' for t in tabs):
                    break
            except Exception:
                time.sleep(0.5)
        if not tabs:
            raise RuntimeError('크롬 CDP 연결 실패 (포트 %d)' % self.port)
        page = next(t for t in tabs if t.get('type') == 'page')
        self.ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=60, suppress_origin=True)
        self.i = 0
        self.events = []
        self.call('Page.enable')
        self.call('Runtime.enable')
        self.call('Emulation.setDeviceMetricsOverride', width=width, height=height, deviceScaleFactor=2, mobile=mobile)

    def call(self, method, **params):
        self.i += 1
        my = self.i
        self.ws.send(json.dumps({'id': my, 'method': method, 'params': params}))
        while True:
            m = json.loads(self.ws.recv())
            if 'method' in m:
                self.events.append(m)
                continue
            if m.get('id') == my:
                if 'error' in m:
                    raise RuntimeError('%s: %s' % (method, m['error']))
                return m.get('result', {})

    def goto(self, url, wait=6):
        self.call('Page.navigate', url=url)
        time.sleep(wait)
        self.pump()

    def pump(self, secs=0.5):
        """쌓인 이벤트를 비운다 (네트워크 응답 수집용)."""
        self.ws.settimeout(secs)
        try:
            while True:
                m = json.loads(self.ws.recv())
                if 'method' in m:
                    self.events.append(m)
        except Exception:
            pass
        self.ws.settimeout(60)

    def bodies(self, pattern):
        """URL 에 pattern 이 든 응답 본문들 (Network.enable 후 goto)."""
        out = []
        for e in list(self.events):
            if e['method'] == 'Network.responseReceived' and pattern in e['params']['response']['url']:
                try:
                    out.append(self.call('Network.getResponseBody', requestId=e['params']['requestId']).get('body', ''))
                except Exception:
                    pass
        return out

    def js(self, expr):
        r = self.call('Runtime.evaluate', expression=expr, returnByValue=True, awaitPromise=True)
        return r.get('result', {}).get('value')

    def shot(self, path):
        import base64
        d = self.call('Page.captureScreenshot', format='png')['data']
        open(path, 'wb').write(base64.b64decode(d))

    def close(self):
        try:
            self.call('Browser.close')
        except Exception:
            pass
        try:
            self.proc.wait(timeout=10)
        except Exception:
            pass
        if not self.keep:
            shutil.rmtree(self.prof, ignore_errors=True)
