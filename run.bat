@echo off
REM Fam Tree Bot - Quick Start Script for Windows
REM ================================================

echo ======================================
echo 🌳 FAM TREE BOT - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.9 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo 📝 IMPORTANT: Please edit .env and set your BOT_TOKEN!
    echo    Get your bot token from @BotFather on Telegram
    echo.
    pause
    exit /b 1
)

REM Check if BOT_TOKEN is set
findstr /C:"your_bot_token_here" .env >nul
if not errorlevel 1 (
    echo 📝 Please edit .env and set your BOT_TOKEN!
    echo    Get your bot token from @BotFather on Telegram
    pause
    exit /b 1
)

REM Run the bot
echo.
echo 🚀 Starting Fam Tree Bot...
echo ======================================
python bot.py

pause
