#!/bin/bash
# Setup script for MERCUR-E GitHub Bot

set -e

echo "🚀 Setting up MERCUR-E GitHub Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your GitHub App credentials"
fi

# Check for private key
if [ ! -f "private-key.pem" ]; then
    echo "⚠️  WARNING: private-key.pem not found!"
    echo "   Please download your GitHub App private key and save it as private-key.pem"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your GitHub App credentials"
echo "2. Place your GitHub App private key as private-key.pem"
echo "3. Run './run_local.sh' to start the bot locally"
echo "4. Use ngrok or Cloudflare Tunnel to expose webhook endpoint"
echo ""
