@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [Weekly AI 봇 설치 점검]
echo.

where python >nul 2>nul || (echo [X] python 없음 - python 3.11 이상을 설치하세요 ^(python.org^) & goto :end)
python --version

echo.
echo [1/2] 파이썬 패키지 설치
python -m pip install -r requirements.txt || python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

echo.
echo [2/2] 프로그램 확인
set CH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CH=1
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set CH=1
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set CH=1
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" set CH=1
if defined CH (echo [O] Chrome/Edge) else (echo [X] Chrome/Edge 없음 - 캡처·인스타 받기에 필요)
where node >nul 2>nul && (echo [O] node) || echo [!] node 없음 - 유튜브 받기에 필요 ^(nodejs.org^)
where gh >nul 2>nul && (echo [O] gh - 배포하려면 gh auth login) || echo [!] gh 없음 - "올려줘" 배포에만 필요 ^(cli.github.com^)
where claude >nul 2>nul && (echo [O] claude) || echo [!] Claude Code 없음 - claude.com/claude-code

echo.
echo 완료. 이 폴더에서 claude 를 실행하고  /weeklyai ^<URL^>  로 시작하세요.
:end
pause
