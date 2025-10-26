#!/bin/bash
# Run MERCUR-E GitHub Bot locally

set -e

echo "🚀 Starting MERCUR-E GitHub Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check for .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Check for private key
if [ ! -f "private-key.pem" ]; then
    echo "❌ private-key.pem not found. Please add your GitHub App private key."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the application
echo "✅ Starting server..."
python -m mercur_e.main
