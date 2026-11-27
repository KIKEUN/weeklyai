# -*- coding: utf-8 -*-
"""본문 AI 티 점검 — im-not-ai(humanize-korean) 진단 shim 을 카드 본문에 돌린다 (가이드 §9-4 C).

사용: python humanize_check.py 34
  → _workspace/volN-humanize/ 에 01_input.txt(제목+본문) · 00_metrics.json 생성, 위험도와 걸린 지표 출력.
  route_hint 가 light 가 아니거나 경고 지표가 있으면 humanize-korean 스킬 규칙으로 cards.py 본문을 고친다
  (내용·수치·고유명사 불변, 줄 34자·6줄 규칙 유지). 스킬 설치: .claude/skills/humanize-korean (epoko77-ai/im-not-ai, MIT)
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wai import load_spec, utf8_stdout, vol_dir

utf8_stdout()
D = vol_dir(sys.argv[1] if len(sys.argv) > 1 else '.')
S = load_spec(D)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
SHIM = os.path.join(ROOT, '.claude', 'skills', 'humanize-korean', 'scripts', 'prepare_monolith_input.py')
if not os.path.exists(SHIM):
    sys.exit('humanize-korean 미설치: %s' % SHIM)
run = os.path.join(ROOT, '_workspace', 'vol%d-humanize' % S.VOL)
os.makedirs(run, exist_ok=True)
# 줄바꿈은 카드 폭 때문이므로 한 문단으로 이어 붙여 문장 단위로 보게 한다
txt = '\n\n'.join(re.sub(r'<[^>]+>', '', ' '.join(x for b in c['body'] for x in ([b] if isinstance(b, str) else b))) for c in S.CARDS)
open(os.path.join(run, '01_input.txt'), 'w', encoding='utf-8').write(txt + '\n')
r = subprocess.run([sys.executable, SHIM, '--run-dir', run, '--genre', 'news'], capture_output=True, text=True,
                   encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
m = json.load(open(os.path.join(run, '00_metrics.json'), encoding='utf-8'))
print('VOL.%d 본문 AI 티 점검 — 위험도 %s (점수 %s), 경로 %s' % (S.VOL, m.get('risk_band'), m.get('risk_score'),
      re.search(r'route_hint=(\w+)', r.stdout).group(1) if 'route_hint=' in r.stdout else '?'))
WARN = {  # z 절댓값 2 이상만 — 사람 뉴스 글 기준선 대비 튀는 지표
    'ending_comma_rate': '쉼표로 이어 붙인 문장이 많음 → 일부는 마침표로 끊거나 연결어미를 바꾼다',
    'ending_diversity': '종결이 "~습니다"로 단조 — 카드 존댓말 특성상 어느 정도 남는다. 문장 길이를 섞어(나누기·합치기) 리듬만 준다',
    'comma_usage_rate': '쉼표 사용이 많음',
    'hanja_nominalizer_density': '한자어 명사화(~화·~성·~적) 과다', 'normalisation_score': '명사화 문체 과다',
    'inanimate_subject_rate': '무생물 주어(번역투) 과다', 'by_passive_count': '"~에 의해" 피동 과다',
    'double_passive_count': '이중 피동 과다', 'da_streak_rate': '같은 종결어미 연속',
}
z = dict(m.get('z_scores', {})); z.update({k: v for k, v in (m.get('v2_z_scores') or {}).items() if v is not None})
LOW_BAD = {'ending_diversity'}   # 이 지표만 낮을수록 나쁨, 나머지는 높을수록(사람 글보다 많을수록) 나쁨
hit = [(k, v) for k, v in z.items() if k in WARN and (v <= -2 if k in LOW_BAD else v >= 2)]
for k, v in sorted(hit, key=lambda x: -abs(x[1])):
    print('  - %s (z %+.1f): %s' % (k, v, WARN[k]))
for e in (m.get('evidence') or {}).get('conclusion_pivots', [])[:5]:
    print('  - 결론 전환 상투구: %s' % e)
print('  자료: %s' % os.path.relpath(run, ROOT))
