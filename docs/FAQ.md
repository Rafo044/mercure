# ❓ Frequently Asked Questions - MERCUR-E GitHub Bot

## General Questions

### What is MERCUR-E GitHub Bot?

MERCUR-E is a fully functional GitHub App that automates repository management through slash commands, GitHub Actions integration, and AI-powered insights.

### What can it do?

- Trigger GitHub Actions workflows with `/test`
- Merge pull requests automatically with `/merge`
- Generate comprehensive reports with `/report`
- Integrate with AI assistants via FastMCP
- Validate webhooks securely
- Support PAM authentication for privileged operations

### Is it free?

Yes, the bot is open source and free to use. You only need a GitHub account to create a GitHub App.

## Setup Questions

### How do I create a GitHub App?

1. Go to GitHub Settings → Developer settings → GitHub Apps
2. Click "New GitHub App"
3. Fill in the required information
4. Set permissions (see README.md)
5. Subscribe to events (issue_comment, pull_request, push)
6. Generate and download private key

### Where do I get the App ID?

After creating your GitHub App:
1. Go to the app's settings page
2. The App ID is shown at the top of the page
3. Copy it to your `.env` file

### What is the webhook secret?

The webhook secret is a password that GitHub uses to sign webhook payloads. You set this when creating your GitHub App. Use a strong, random string.

Generate one:
```bash
openssl rand -hex 32
```

### Where is the private key?

When you create a GitHub App and click "Generate private key", GitHub downloads a `.pem` file. Save this as `private-key.pem` in your project directory.

## Installation Questions

### What Python version do I need?

Python 3.8 or higher. Check your version:
```bash
python3 --version
```

### Do I need Docker?

No, Docker is optional. You can run the bot with:
- Python virtual environment (recommended for development)
- Docker (recommended for production)
- systemd service

### Can I run this on Windows?

Yes, but the setup scripts are written for Linux/Mac. On Windows:
1. Create venv manually: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python main.py`

### Installation fails with dependency errors

Update pip first:
```bash
./venv/bin/pip install --upgrade pip
```

Then retry:
```bash
./venv/bin/pip install -r requirements.txt
```

## Configuration Questions

### What environment variables are required?

Minimum required:
```env
GITHUB_APP_ID=your_app_id
GITHUB_WEBHOOK_SECRET=your_secret
```

The bot will use defaults for other settings.

### Can I use a different port?

Yes, edit `.env`:
```env
PORT=9000
```

### How do I enable debug logging?

Edit `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Running Questions

### How do I test locally?

1. Start the bot: `./run_local.sh`
2. In another terminal, start ngrok: `ngrok http 8000`
3. Update GitHub App webhook URL with ngrok URL
4. Test on a repository where the app is installed

### What is ngrok?

ngrok creates a secure tunnel to your localhost, allowing GitHub to send webhooks to your local development machine.

Download: https://ngrok.com/download

### Can I use something other than ngrok?

Yes, alternatives:
- Cloudflare Tunnel (free, no account needed)
- localtunnel
- serveo
- Your own reverse proxy

### The bot starts but doesn't respond to commands

Check:
1. Is the app installed on the repository?
2. Is the webhook URL correct?
3. Are webhooks being delivered? (Check GitHub App settings → Advanced → Recent Deliveries)
4. Check logs: `tail -f logs/githubbot.log`

## Command Questions

### What commands are available?

- `/test [workflow]` - Trigger GitHub Actions workflow
- `/merge [method]` - Merge PR (squash/merge/rebase)
- `/report` - Generate status report

### Can I add custom commands?

Yes! Edit `commands.py` to add new command handlers, then register them in `main.py`.

### Why isn't `/merge` working?

Check:
1. Is it used on a pull request (not an issue)?
2. Is the PR mergeable (no conflicts)?
3. Does the bot have `pull_requests: write` permission?
4. Are CI checks passing?

### Can I use multiple commands in one comment?

Yes! Each command on its own line:
```
/test ci.yml
/report
```

## Permissions Questions

### What permissions does the bot need?

Repository permissions:
- Actions: Read & write
- Contents: Read & write
- Issues: Read & write
- Pull requests: Read & write
- Workflows: Read & write

### Can the bot delete files?

No, the bot is designed to only read and write files, not delete them. This is a safety feature.

### Can I restrict who can use commands?

Currently, anyone with write access to the repository can use commands. You can add custom authorization logic in `commands.py`.

## Security Questions

### Is the webhook signature validated?

Yes, all webhooks are validated using HMAC-SHA256 (or SHA1 for legacy).

### How is authentication handled?

The bot uses:
1. GitHub App JWT for app-level authentication
2. Installation tokens for repository access
3. Optional PAM for privileged operations

### Should I use HTTPS in production?

Absolutely! Use Let's Encrypt for free SSL certificates. See DEPLOYMENT.md for setup instructions.

### What is PAM authentication?

PAM (Pluggable Authentication Modules) provides an additional layer of authentication for privileged operations. It's optional and disabled by default.

## AI Integration Questions

### What is FastMCP?

FastMCP is a framework for exposing tools to AI assistants. It allows AI models to interact with your GitHub bot programmatically.

### How do I enable AI integration?

1. Start the MCP server: `./run_mcp.sh`
2. Configure your AI assistant to connect to `http://localhost:8001`

### Which AI assistants are supported?

Any AI assistant that supports the MCP protocol:
- Claude Desktop
- Custom GPT implementations
- Any MCP-compatible client

### Can AI assistants execute commands directly?

No, AI assistants can only:
- Parse comments
- Analyze PRs
- Suggest commands
- Generate reports

Actual command execution requires a human to post the command in a GitHub comment.

## Deployment Questions

### How do I deploy to production?

See DEPLOYMENT.md for complete instructions. Quick summary:
1. Set up a server with Docker
2. Configure domain and DNS
3. Obtain SSL certificate with Let's Encrypt
4. Deploy with Docker Compose
5. Update GitHub App webhook URL

### What are the server requirements?

Minimum:
- 1 CPU core
- 512 MB RAM
- 10 GB disk space
- Ubuntu 20.04+ or similar Linux distribution

### Can I deploy to Heroku/Railway/Render?

Yes! The bot works on any platform that supports:
- Python 3.8+
- Persistent storage for logs
- Inbound HTTPS connections

### How do I update the bot?

```bash
cd /opt/mercur-e-bot
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

## Troubleshooting Questions

### Webhook signature validation fails

1. Check webhook secret matches in GitHub App and `.env`
2. Verify no extra spaces in secret
3. Check GitHub is sending SHA-256 signature
4. Review logs for exact error

### "Installation not found" error

1. Install the app on the repository
2. Verify installation ID is correct
3. Check app has required permissions

### Commands execute but nothing happens

1. Check bot has required permissions
2. Verify GitHub Actions workflows exist
3. Review logs for errors
4. Check API rate limits

### High memory usage

1. Check for memory leaks in custom code
2. Limit concurrent webhook processing
3. Add resource limits in Docker
4. Monitor with `docker stats`

### Logs are too large

Configure log rotation in `/etc/logrotate.d/mercur-e-bot`:
```
/opt/mercur-e-bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
}
```

## Performance Questions

### How many requests can it handle?

Depends on your server, but the bot can handle:
- 100+ webhooks per minute
- 1000+ API requests per hour (GitHub rate limit)

### Can I scale horizontally?

Yes, but you'll need:
- Load balancer
- Shared storage for logs
- Redis for token caching (not implemented by default)

### How do I monitor performance?

1. Check logs: `tail -f logs/githubbot.log`
2. Monitor Docker: `docker stats`
3. Use APM tools like Datadog, New Relic
4. Set up health check monitoring

## Advanced Questions

### Can I use this with GitHub Enterprise?

Yes, update the GitHub API base URL in `github_auth.py`:
```python
Github(token, base_url="https://github.enterprise.com/api/v3")
```

### Can I integrate with other services?

Yes! Add integrations in `commands.py` or create new modules. Examples:
- Slack notifications
- Jira integration
- Custom CI/CD systems

### Can I use a database?

Yes, add database support for:
- Event history
- User preferences
- Command audit logs
- Analytics

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support Questions

### Where can I get help?

1. Check this FAQ
2. Review README.md and other documentation
3. Check logs for error messages
4. Search GitHub issues
5. Create a new issue with details

### How do I report a bug?

Create a GitHub issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Log excerpts (remove sensitive data)
- Environment details (OS, Python version, etc.)

### Can I request features?

Yes! Create a GitHub issue with:
- Feature description
- Use case
- Expected behavior
- Any relevant examples

---

Still have questions? Check the documentation or create an issue!
