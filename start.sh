#!/bin/bash

set -e  # stop if anything fails

echo "🚀 Setting up environment..."

# create venv (optional but recommended)
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# activate venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎭 Installing Playwright browsers..."
playwright install

echo "⚡ Running scraper..."
python scrapping_with_playwright.py   

echo "✅ Done!"