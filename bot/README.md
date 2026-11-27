# Weekly AI 카드뉴스 봇 (/weeklyai)

인스타 게시물·공식 발표·뉴스 URL을 주면 Claude Code가 다음 호 카드뉴스(`weeklyaivolN.html`, 540×720 캐러셀)와 갑지를 만들어 주는 봇입니다. 이 저장소에 올라간 vol1~ 카드뉴스가 이 봇으로 만든 결과물입니다.

## 들어 있는 것
| 경로 | 내용 |
|---|---|
| `.claude/skills/weeklyai/` | 봇 본체 (SKILL.md, 스크립트, 템플릿) |
| `.claude/skills/humanize-korean/` 외 3개, `.claude/agents/` | 글 윤문 스킬 im-not-ai (아래 출처) |
| `카드뉴스_제작가이드.md` | 규칙의 정본 — 봇이 작업 전에 반드시 읽음 |
| `갑지_제작가이드.md` | 갑지(표지) 규칙 |

## 봇이 지키는 세 가지
1. **작업 전에 제작가이드 두 개를 끝까지 먼저 읽고** 시작합니다.
2. **글(표지·소개·제목·본문·갑지 문구)을 쓸 땐 무조건 im-not-ai(humanize-korean) 스킬로 윤문**한 뒤 넣습니다.
3. **문맥을 끊지 않습니다.** 단문을 뚝뚝 자르지 않고 앞뒤 문장을 이어 한 흐름으로 씁니다.

## 설치
1. 이 `bot/` 폴더 안의 내용(`.claude` 폴더와 가이드 2개)을 카드뉴스 작업 폴더(예: `Weekly AI/`)에 그대로 복사합니다. `.claude`는 숨김 폴더일 수 있으니 탐색기에서 숨긴 항목을 켜세요.
   - 저장소 전체는 미디어 때문에 무거우니 `bot/` 폴더만 받는 걸 권합니다:
     ```
     git clone --depth 1 --filter=blob:none --sparse https://github.com/KIKEUN/weeklyai.git
     cd weeklyai && git sparse-checkout set bot
     ```
2. 파이썬 패키지 (python 3.11 이상):
   ```
   pip install pillow imageio-ffmpeg websocket-client yt-dlp
   ```
   사내망에서 인증서 오류가 나면 `--trusted-host pypi.org --trusted-host files.pythonhosted.org` 를 붙입니다.
3. 필요 프로그램: Chrome(또는 Edge), node.js(유튜브 받기용), 배포하려면 GitHub CLI `gh` (`gh auth login`).
4. 그 폴더에서 Claude Code를 실행합니다.

## 사용
- `/weeklyai <인스타·공식 발표·뉴스·유튜브 URL>` 또는 "이걸로 weeklyai 만들자 <URL>"
- 봇이 가이드를 읽고, 다음 호 번호(`volN`)를 정해 구성안 표를 보여준 뒤 `volN/weeklyaivolN.html` 을 만듭니다.
- 수정은 말로("3장 제목 바꿔줘"), 배포는 "올려줘".
- 인스타 소스는 처음 한 번 로그인이 필요합니다:
  ```
  ! python .claude/skills/weeklyai/scripts/fetch_insta.py --login
  ```

## 내 저장소에 배포하려면
`.claude/skills/weeklyai/scripts/publish.py` 의 `REPO = 'KIKEUN/weeklyai'` 를 본인 저장소로 바꾸고, 그 저장소에 GitHub Pages를 켜 두세요. 표지 로고는 `kikeun.github.io/weeklyai/assets/ai54.png` 를 참조합니다.

## 출처
- 윤문 스킬 humanize-korean·humanize·humanize-scan·humanize-redo 및 에이전트 4개: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (MIT License). 최신판은 원본 저장소에서 `CLAUDE_HOME=<작업폴더>/.claude bash install.sh --claude-only --copy` 로 받을 수 있습니다.
