# Changelog

All notable changes to MERCUR-E will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-26

### 🎉 Initial Release

#### ✨ Added

- **Core Features**
  - FastAPI-based webhook server
  - GitHub App authentication with JWT
  - Webhook signature validation (SHA-256 & SHA-1)
  - Event handling for issue_comment, pull_request, and push events

- **Slash Commands**
  - `/test [workflow]` - Trigger GitHub Actions workflows
  - `/merge [method]` - Merge pull requests with validation
  - `/report` - Generate comprehensive status reports

- **AI Integration**
  - FastMCP server for AI assistant integration
  - 5 MCP tools for PR analysis and command suggestions
  - Natural language command parsing

- **Security**
  - HMAC webhook signature validation
  - JWT-based GitHub App authentication
  - Optional PAM authentication
  - TLS/HTTPS support with Let's Encrypt
  - Rate limiting via nginx

- **Deployment**
  - Docker support with Dockerfile
  - Docker Compose configuration
  - Nginx reverse proxy with TLS
  - systemd service file
  - Health check endpoints

- **Testing**
  - Comprehensive test suite with pytest
  - 15+ unit tests
  - Coverage reporting
  - GitHub Actions CI/CD

- **Documentation**
  - Detailed README with visual elements
  - Quick Start Guide
  - Deployment Guide
  - Testing Guide
  - AI Integration Guide
  - FAQ
  - Contributing Guidelines
  - Azerbaijani documentation

#### 🔧 Technical

- Modern Python packaging with pyproject.toml
- Testable code structure with dependency injection
- Relative imports for package structure
- Entry points for CLI commands
- Black code formatting
- Flake8 linting
- Type hints support

#### 📦 Dependencies

- FastAPI 0.109.0
- PyGithub 2.1.1
- FastMCP 0.1.0
- Uvicorn 0.27.0
- Pydantic 2.10.5
- And more...

---

## [Unreleased]

### 🚧 Planned Features

- [ ] Database integration for event history
- [ ] Web dashboard for monitoring
- [ ] Additional slash commands (/deploy, /rollback)
- [ ] Custom command permissions
- [ ] Slack/Discord notifications
- [ ] Jira integration
- [ ] Advanced PR analytics
- [ ] Multi-repository support

---

[1.0.0]: https://github.com/Rafo044/mercur-e/releases/tag/v1.0.0
