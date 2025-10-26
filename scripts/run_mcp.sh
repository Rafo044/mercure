#!/bin/bash
# Run FastMCP server for AI integration

set -e

echo "🤖 Starting FastMCP server for AI integration..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run MCP server
echo "✅ Starting MCP server..."
python -m mercur_e.mcp_server
