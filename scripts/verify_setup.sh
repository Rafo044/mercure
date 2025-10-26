#!/bin/bash
# Verification script for MERCUR-E GitHub Bot setup

echo "🔍 Verifying MERCUR-E GitHub Bot Setup..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        ((FAILED++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        ((FAILED++))
        return 1
    fi
}

# Function to check command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        ((PASSED++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 not found (optional)"
        ((WARNINGS++))
        return 1
    fi
}

echo "📁 Checking Core Files..."
check_file "main.py"
check_file "config.py"
check_file "github_auth.py"
check_file "security.py"
check_file "commands.py"
check_file "mcp_server.py"
check_file "requirements.txt"

echo ""
echo "🐳 Checking Deployment Files..."
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file "nginx.conf"
check_file "mercur-e-bot.service"

echo ""
echo "📜 Checking Scripts..."
check_file "setup.sh"
check_file "run_local.sh"
check_file "run_mcp.sh"
check_file "Makefile"

echo ""
echo "📚 Checking Documentation..."
check_file "README.md"
check_file "QUICKSTART.md"
check_file "DEPLOYMENT.md"
check_file "TESTING.md"
check_file "AI_INTEGRATION.md"
check_file "FAQ.md"
check_file "CONTRIBUTING.md"
check_file "PROJECT_SUMMARY.md"
check_file "LICENSE"

echo ""
echo "⚙️  Checking Configuration..."
check_file ".env.example"
check_file ".gitignore"

echo ""
echo "📂 Checking Directories..."
check_dir "venv"
check_dir "examples"

echo ""
echo "🔧 Checking System Requirements..."
check_command "python3"
check_command "pip3"
check_command "docker"
check_command "docker-compose"
check_command "ngrok"

echo ""
echo "🔐 Checking Credentials..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    ((PASSED++))
    
    # Check if required variables are set
    if grep -q "GITHUB_APP_ID=" .env && ! grep -q "GITHUB_APP_ID=your_app_id" .env; then
        echo -e "${GREEN}✓${NC} GITHUB_APP_ID is configured"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} GITHUB_APP_ID needs to be configured"
        ((WARNINGS++))
    fi
    
    if grep -q "GITHUB_WEBHOOK_SECRET=" .env && ! grep -q "GITHUB_WEBHOOK_SECRET=your_webhook_secret" .env; then
        echo -e "${GREEN}✓${NC} GITHUB_WEBHOOK_SECRET is configured"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} GITHUB_WEBHOOK_SECRET needs to be configured"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} .env file not found (copy from .env.example)"
    ((WARNINGS++))
fi

if [ -f "private-key.pem" ]; then
    echo -e "${GREEN}✓${NC} private-key.pem exists"
    ((PASSED++))
    
    # Check file permissions
    PERMS=$(stat -c %a private-key.pem 2>/dev/null || stat -f %A private-key.pem 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        echo -e "${GREEN}✓${NC} private-key.pem has correct permissions (600)"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} private-key.pem permissions should be 600 (currently $PERMS)"
        echo "  Run: chmod 600 private-key.pem"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} private-key.pem not found (download from GitHub App)"
    ((WARNINGS++))
fi

echo ""
echo "📦 Checking Python Dependencies..."
if [ -d "venv" ]; then
    if [ -f "venv/bin/python" ]; then
        INSTALLED=$(./venv/bin/pip list 2>/dev/null | wc -l)
        if [ "$INSTALLED" -gt 10 ]; then
            echo -e "${GREEN}✓${NC} Dependencies installed ($INSTALLED packages)"
            ((PASSED++))
        else
            echo -e "${YELLOW}⚠${NC} Dependencies may not be fully installed"
            echo "  Run: ./venv/bin/pip install -r requirements.txt"
            ((WARNINGS++))
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found"
    echo "  Run: ./setup.sh"
    ((WARNINGS++))
fi

echo ""
echo "📊 Verification Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Setup is complete! You're ready to run the bot.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Configure .env with your GitHub App credentials (if not done)"
    echo "2. Add private-key.pem from your GitHub App (if not done)"
    echo "3. Run: ./run_local.sh"
    echo "4. Expose with ngrok: ngrok http 8000"
    echo "5. Update webhook URL in GitHub App settings"
elif [ $FAILED -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Setup is mostly complete, but some warnings need attention.${NC}"
    echo ""
    echo "Review the warnings above and:"
    echo "1. Configure .env if needed"
    echo "2. Add private-key.pem if needed"
    echo "3. Install optional tools if desired"
elif [ $FAILED -lt 5 ]; then
    echo -e "${YELLOW}⚠️  Setup is incomplete. Please address the failed checks.${NC}"
else
    echo -e "${RED}❌ Setup has significant issues. Please run ./setup.sh${NC}"
fi

echo ""
exit 0
