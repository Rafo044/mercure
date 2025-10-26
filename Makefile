# Makefile for MERCUR-E GitHub Bot

.PHONY: help setup install run run-mcp docker-build docker-run docker-stop clean test lint format

help:
	@echo "🤖 MERCUR-E GitHub Bot - Available commands:"
	@echo ""
	@echo "  make setup        - Initial setup (create venv, install deps)"
	@echo "  make install      - Install/update dependencies"
	@echo "  make install-dev  - Install with dev dependencies"
	@echo "  make run          - Run bot locally"
	@echo "  make run-mcp      - Run FastMCP server"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run code linters"
	@echo "  make format       - Format code with black"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run with Docker Compose"
	@echo "  make docker-stop  - Stop Docker containers"
	@echo "  make logs         - View application logs"
	@echo "  make clean        - Clean up temporary files"
	@echo ""

setup:
	@echo "🚀 Setting up MERCUR-E GitHub Bot..."
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

install:
	@echo "📦 Installing dependencies..."
	@./venv/bin/pip install -e .

install-dev:
	@echo "📦 Installing with dev dependencies..."
	@./venv/bin/pip install -e ".[dev]"

run:
	@echo "▶️  Starting bot..."
	@chmod +x scripts/run_local.sh
	@./scripts/run_local.sh

run-mcp:
	@echo "🤖 Starting FastMCP server..."
	@chmod +x scripts/run_mcp.sh
	@./scripts/run_mcp.sh

docker-build:
	@echo "🐳 Building Docker image..."
	@docker build -t mercur-e-bot .

docker-run:
	@echo "🐳 Starting Docker containers..."
	@docker-compose up -d
	@echo "✅ Containers started"
	@docker-compose ps

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	@docker-compose down

docker-logs:
	@docker-compose logs -f

logs:
	@tail -f logs/githubbot.log

clean:
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "✅ Cleanup complete"

test:
	@echo "🧪 Running tests..."
	@./venv/bin/pytest tests/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	@./venv/bin/pytest --cov=mercur_e --cov-report=term-missing --cov-report=html

lint:
	@echo "🔍 Running linters..."
	@./venv/bin/flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	@./venv/bin/black --check src/ tests/

format:
	@echo "✨ Formatting code..."
	@./venv/bin/black src/ tests/

check-env:
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Copy from .env.example"; \
		exit 1; \
	fi
	@if [ ! -f private-key.pem ]; then \
		echo "❌ private-key.pem not found"; \
		exit 1; \
	fi
	@echo "✅ Environment files present"

dev: check-env
	@echo "🔧 Starting development server..."
	@./venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
