@echo off
REM Forex.com Demo Trading Bot Startup Script
REM This script activates the virtual environment and starts the bot

echo ========================================
echo Starting Forex.com Demo Trading Bot
echo ========================================

REM Navigate to project directory
cd /d "%~dp0"

REM Activate virtual environment (if exists)
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using global Python
)

REM Start the bot
echo Starting main_live_bot.py...
python main_live_bot.py

REM If bot exits, pause to see error
if errorlevel 1 (
    echo.
    echo ========================================
    echo Bot exited with error!
    echo ========================================
    pause
)
