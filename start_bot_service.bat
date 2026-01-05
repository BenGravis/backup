@echo off
REM 5ers Trading Bot - Windows Service Startup Script
REM Works with Task Scheduler SYSTEM account

echo ========================================
echo 5ers Trading Bot Service
echo ========================================

REM Navigate to project directory
cd /d C:\Users\Administrator\botcreativehub

REM Set Python path explicitly
set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

REM Check if Python exists
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    echo Please update the PYTHON variable in this script
    exit /b 1
)

REM Start the bot with logging
echo Starting main_live_bot.py...
echo Log file: bot_output.log
"%PYTHON%" main_live_bot.py >> bot_output.log 2>&1
