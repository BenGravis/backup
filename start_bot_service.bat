@echo off
setlocal enabledelayedexpansion
REM 5ers Trading Bot - Windows Service Startup Script
REM Single-instance guard + venv support

echo ========================================
echo 5ers Trading Bot Service
echo ========================================

REM Navigate to correct project directory
cd /d C:\botcreativehub

REM Single-instance guard: if a python process already runs main_live_bot.py, exit
for /f "tokens=1 delims= " %%A in ('wmic process where "name='python.exe' and CommandLine like '%%main_live_bot.py%%'" get ProcessId ^| findstr /r "^[0-9][0-9]*"') do (
    echo Bot already running (PID %%A). Exiting to prevent duplicate.
    exit /b 0
)

REM Resolve Python path (prefer venv, fallback to global)
if exist "venv\Scripts\python.exe" (
    set PYTHON=venv\Scripts\python.exe
    echo Using venv Python
) else if not defined PYTHON (
    for /f "delims=" %%P in ('where python 2^>nul') do set PYTHON=%%P
)
if not defined PYTHON set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

REM Check if Python exists
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    echo Please install Python or update path
    exit /b 1
)

REM Ensure logs directory exists
if not exist logs mkdir logs

REM Start the bot with logging (append)
echo Starting main_live_bot.py at %date% %time%
echo Using Python: %PYTHON%
echo Log file: logs\bot_output.log
"%PYTHON%" main_live_bot.py >> logs\bot_output.log 2>&1

endlocal
