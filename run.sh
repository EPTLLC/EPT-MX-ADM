#!/bin/bash
#
# Project: EPT-MX-ADM
# Company: EasyProTech LLC (www.easypro.tech)
# Dev: Brabus
# Date: Thu 23 Oct 2025 22:56:11 UTC
# Status: Quick Start Script
# Telegram: https://t.me/EasyProTech
#

# EPT-MX-ADM Quick Start Script

echo "🚀 EPT-MX-ADM Startup Script"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

# Check if static assets exist
if [ ! -d "static/vendor/bootstrap" ]; then
    echo "⚠️  Static assets not found!"
    echo "📦 Downloading static assets..."
    chmod +x install_assets.sh
    ./install_assets.sh
else
    echo "✅ Static assets found"
fi

# Check config.json
if [ ! -f "config.json" ]; then
    echo "❌ config.json not found!"
    echo "Please create config.json first"
    exit 1
fi

MATRIX_SERVER=$(grep -oP '"matrix_server":\s*"\K[^"]+' config.json)
echo "📡 Matrix Server: $MATRIX_SERVER"

if [ "$MATRIX_SERVER" == "https://matrix.example.com" ]; then
    echo "⚠️  WARNING: Please configure your Matrix server in config.json"
fi

echo ""
echo "🎯 Starting EPT-MX-ADM..."
echo "================================"
echo "Access the panel at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

# Run the application
python app.py

