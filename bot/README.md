# Weekly AI 카드뉴스 봇 (/weeklyai)

인스타 게시물·공식 발표·뉴스 URL을 주면 Claude Code가 다음 호 카드뉴스(`weeklyaivolN.html`, 540×720 캐러셀)와 갑지를 만들어 주는 봇입니다. 이 저장소의 vol1~ 카드뉴스가 이 봇으로 만든 결과물입니다.

**이 `bot/` 폴더 자체가 바로 쓰는 작업 폴더입니다.** 받아서 `설치.bat` 한 번 돌리고, 그 폴더에서 `claude` 를 켜고 URL만 주면 됩니다.

## 3분 시작
1. `bot/` 폴더만 받기 (저장소 전체는 미디어 때문에 무거움):
   ```
   git clone --depth 1 --filter=blob:none --sparse https://github.com/KIKEUN/weeklyai.git
   cd weeklyai
   git sparse-checkout set bot
   cd bot
   ```
   git이 없으면 GitHub 웹에서 Code → Download ZIP 후 `bot` 폴더만 꺼내도 됩니다.
2. `설치.bat` 더블클릭 — 파이썬 패키지를 설치하고 Chrome·node·gh·Claude Code가 있는지 알려 줍니다.
3. 이 폴더에서 `claude` 실행 →
   ```
   /weeklyai https://www.instagram.com/p/....
   ```
   봇이 가이드를 읽고, 구성안 표를 보여 준 뒤 `vol1/weeklyaivol1.html` 을 만듭니다. 브라우저로 열어 확인하세요.
4. 수정은 말로("3장 제목 바꿔줘"), 배포는 "올려줘".

## 들어 있는 것
| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | Claude가 이 폴더에서 자동으로 읽는 규칙 (봇 사용·가이드 먼저·윤문 필수) |
| `.claude/skills/weeklyai/` | 봇 본체 — SKILL.md, 스크립트, 템플릿, 최근 호 예시(`examples/vol30~34/cards.py`) |
| `.claude/skills/humanize-korean/` 외 3개, `.claude/agents/` | 글 윤문 스킬 im-not-ai |
| `.claude/settings.json` | 봇 스크립트 실행 허용 (권한 질문 줄이기) |
| `카드뉴스_제작가이드.md`, `갑지_제작가이드.md` | 규칙의 정본 — 봇이 작업 전에 반드시 읽음 |
| `설치.bat`, `requirements.txt` | 설치 점검 |

## 봇이 지키는 세 가지
1. **작업 전에 제작가이드 두 개를 끝까지 먼저 읽고** 시작합니다.
2. **글(표지·소개·제목·본문·갑지 문구)을 쓸 땐 무조건 im-not-ai(humanize-korean) 스킬로 윤문**한 뒤 넣습니다.
3. **문맥을 끊지 않습니다.** 단문을 뚝뚝 자르지 않고 앞뒤 문장을 이어 한 흐름으로 씁니다.

## 필요한 것
- Windows, python 3.11 이상, Claude Code
- Chrome 또는 Edge (공식 페이지 캡처·인스타 받기). 다른 위치에 깔려 있으면 환경변수 `WAI_CHROME` 에 chrome.exe 경로
- node.js (유튜브 받기), GitHub CLI `gh` (배포할 때만)
- 사내망에서 pip 인증서 오류가 나면 `설치.bat` 이 `--trusted-host` 로 다시 시도합니다.

## 인스타 소스
처음 한 번 로그인이 필요합니다. Claude 입력창에:
```
! python .claude/skills/weeklyai/scripts/fetch_insta.py --login
```
뜬 창에서 로그인하고 닫으면 이후엔 자동입니다.

## 내 저장소에 배포하려면
"올려줘"는 `.claude/skills/weeklyai/scripts/publish.py` 의 `REPO = 'KIKEUN/weeklyai'` 로 올립니다. 쓰기 권한이 없으면 실패하니, 본인 저장소 이름으로 바꾸고 그 저장소에 GitHub Pages를 켜 두세요. 표지 로고는 `kikeun.github.io/weeklyai/assets/ai54.png` 를 그대로 참조합니다.

## 출처
- 윤문 스킬 humanize-korean·humanize·humanize-scan·humanize-redo 및 에이전트 4개: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (MIT License).
