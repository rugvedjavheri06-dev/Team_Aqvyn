@echo off
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
title Aqvyn paper desk - live demo with a real LLM

rem --- Real model on RunInfra (OpenAI-compatible). The key is asked for every time and is NEVER written to a file. ---
set AGENTX_LLM_BASE_URL=https://api.runinfra.ai/v1
set AGENTX_LLM_MODEL=deepseek-v4-1-flash-1017
set AGENTX_LLM_TIMEOUT=90
set AGENTX_LLM_API_KEY=

echo.
echo Paste your RunInfra key (it will NOT show on screen) and press Enter.
for /f "delims=" %%i in ('powershell -NoProfile -Command "$s=Read-Host -AsSecureString 'RunInfra key'; [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))"') do set AGENTX_LLM_API_KEY=%%i
if "%AGENTX_LLM_API_KEY%"=="" (
  set /p AGENTX_LLM_API_KEY=Could not hide input. Type the key and press Enter: 
  cls
)

where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% -c "import numpy" >nul 2>nul || %PY% -m pip install numpy

echo.
echo [1/2] Checking the model answers...
%PY% -m agentx.check_llm
if errorlevel 1 (
  echo.
  echo The model check failed. Fix that first, the dashboard would fall back to rules only.
  pause
  exit /b 1
)

echo.
echo [2/2] Starting the dashboard on market seed 18 at http://localhost:8765  (Ctrl+C here to stop)
start "" http://localhost:8765
%PY% -m agentx.dashboard --llm http --seed 18 --port 8765
