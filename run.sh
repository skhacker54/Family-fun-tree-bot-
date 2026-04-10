#!/bin/bash
# Fam Tree Bot - Quick Start Script
# ===================================

set -e

echo "======================================"
echo "🌳 FAM TREE BOT - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 IMPORTANT: Please edit .env and set your BOT_TOKEN!"
    echo "   Get your bot token from @BotFather on Telegram"
    echo ""
    exit 1
fi

# Check if BOT_TOKEN is set
if grep -q "your_bot_token_here" .env; then
    echo "📝 Please edit .env and set your BOT_TOKEN!"
    echo "   Get your bot token from @BotFather on Telegram"
    exit 1
fi

# Run the bot
echo ""
echo "🚀 Starting Fam Tree Bot..."
echo "======================================"
python3 bot.py
