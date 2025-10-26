<div align="center">

# 🤖 MERCUR-E

### AI-Powered GitHub Bot for Intelligent Repository Automation

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<img src="./assets/banner.svg" alt="MERCUR-E Banner" width="800"/>

**Automate your GitHub workflow with slash commands, AI insights, and intelligent PR management**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 **Core Capabilities**

- **Slash Commands** - Control your repo with simple comments
  - `/test` - Trigger GitHub Actions workflows
  - `/merge` - Smart PR merging with validation
  - `/report` - Comprehensive status reports

- **Event Handling** - Responds to:
  - 💬 Issue comments
  - 🔀 Pull requests
  - 📤 Push events

</td>
<td width="50%">

### 🤖 **AI Integration**

- **FastMCP Server** - AI assistant ready
- **Intelligent Analysis** - PR insights & suggestions
- **Natural Language** - Command parsing
- **Automated Reports** - AI-generated summaries

### 🔒 **Security First**

- ✅ Webhook signature validation
- ✅ JWT authentication
- ✅ TLS/HTTPS support
- ✅ PAM authentication (optional)

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- 🐍 Python 3.11+
- 🔑 GitHub App ([Create one](https://github.com/settings/apps))
- 🔐 Private key from your GitHub App

### Installation

```bash
# Clone the repository
git clone https://github.com/Rafo044/mercur-e.git
cd mercur-e

# Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Configure
cp .env.example .env
nano .env  # Add your GitHub App credentials

# Add private key
cp ~/Downloads/your-app.pem ./private-key.pem
chmod 600 private-key.pem

# Start the bot
./scripts/run_local.sh
```

### Test Locally with ngrok

```bash
# In another terminal
ngrok http 8000

# Update your GitHub App webhook URL with the ngrok HTTPS URL
```

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white) |
| **GitHub** | ![PyGithub](https://img.shields.io/badge/PyGithub-181717?style=flat-square&logo=github&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white) |
| **AI** | ![FastMCP](https://img.shields.io/badge/FastMCP-FF6B6B?style=flat-square&logo=ai&logoColor=white) ![Claude](https://img.shields.io/badge/Claude-8B5CF6?style=flat-square&logo=anthropic&logoColor=white) |
| **Security** | ![Cryptography](https://img.shields.io/badge/Cryptography-3C873A?style=flat-square&logo=letsencrypt&logoColor=white) ![PAM](https://img.shields.io/badge/PAM-FCC624?style=flat-square&logo=linux&logoColor=black) |
| **Deployment** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white) ![Let's Encrypt](https://img.shields.io/badge/Let's%20Encrypt-003A70?style=flat-square&logo=letsencrypt&logoColor=white) |
| **Testing** | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) ![Coverage](https://img.shields.io/badge/Coverage-3C873A?style=flat-square&logo=codecov&logoColor=white) |

</div>

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| 📘 [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| 🚀 [Deployment Guide](docs/DEPLOYMENT.md) | Production deployment with TLS |
| 🧪 [Testing Guide](docs/TESTING.md) | Testing strategies and examples |
| 🤖 [AI Integration](docs/AI_INTEGRATION.md) | FastMCP and AI assistant setup |
| ❓ [FAQ](docs/FAQ.md) | Frequently asked questions |
| 🤝 [Contributing](docs/CONTRIBUTING.md) | How to contribute |
| 🇦🇿 [Azərbaycan](docs/AZƏRBAYCAN_README.md) | Azərbaycan dilində təlimat |

---

## 💡 Usage Examples

### Trigger CI Workflow

```bash
# On any PR or issue, comment:
/test

# Or specify a workflow:
/test ci.yml
```

### Merge Pull Request

```bash
# Merge with squash (default):
/merge

# Or specify merge method:
/merge squash
/merge merge
/merge rebase
```

### Generate Status Report

```bash
# Get comprehensive PR/issue report:
/report
```

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔧 Configuration

### Required Environment Variables

```env
GITHUB_APP_ID=your_app_id
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_APP_PRIVATE_KEY_PATH=./private-key.pem
```

### Optional Settings

```env
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
FASTMCP_ENABLED=True
PAM_ENABLED=False
```

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=mercur_e --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📊 Project Structure

```
mercur-e/
├── src/mercur_e/          # Main application code
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration
│   ├── github_auth.py     # GitHub authentication
│   ├── security.py        # Security utilities
│   ├── commands.py        # Command handlers
│   └── mcp_server.py      # AI integration
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── examples/              # Example configurations
├── .github/               # GitHub workflows
└── pyproject.toml         # Project metadata
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- 🐙 [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API wrapper
- 🤖 [FastMCP](https://github.com/jlowin/fastmcp) - AI integration framework
- 🐳 [Docker](https://www.docker.com/) - Containerization
- 🔒 [Let's Encrypt](https://letsencrypt.org/) - Free SSL certificates

---

## 📞 Support

- 📖 Check the [documentation](docs/)
- 🐛 [Report bugs](https://github.com/Rafo044/mercur-e/issues)
- 💬 [Discussions](https://github.com/Rafo044/mercur-e/discussions)
- ⭐ Star this repo if you find it useful!

---

<div align="center">

**Made with ❤️ by [Claude Sonnet](https://www.anthropic.com/claude)**

[![GitHub stars](https://img.shields.io/github/stars/Rafo044/mercur-e?style=social)](https://github.com/Rafo044/mercur-e/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Rafo044/mercur-e?style=social)](https://github.com/Rafo044/mercur-e/network/members)

</div>
