# 🧪 Testing Guide for MERCUR-E GitHub Bot

## Local Testing with ngrok

### 1. Install ngrok

```bash
# Download from https://ngrok.com/download
# Or use snap:
sudo snap install ngrok
```

### 2. Start the Bot

```bash
# Terminal 1: Start the bot
./run_local.sh
```

### 3. Expose with ngrok

```bash
# Terminal 2: Start ngrok
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### 4. Update GitHub App Webhook

1. Go to your GitHub App settings
2. Update Webhook URL to: `https://abc123.ngrok.io/webhook`
3. Save changes

### 5. Test Commands

Create a test repository and install your GitHub App on it.

#### Test /test Command

1. Create a pull request or issue
2. Add a comment: `/test`
3. Check ngrok terminal for incoming webhook
4. Check bot logs for processing

#### Test /merge Command

1. Create a pull request
2. Ensure CI passes (if you have workflows)
3. Add comment: `/merge squash`
4. PR should be merged

#### Test /report Command

1. On any PR or issue
2. Add comment: `/report`
3. Bot should post a detailed report

## Testing with Cloudflare Tunnel (Alternative to ngrok)

### 1. Install Cloudflare Tunnel

```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### 2. Authenticate

```bash
cloudflared tunnel login
```

### 3. Create Tunnel

```bash
cloudflared tunnel create mercur-e-bot
```

### 4. Configure Tunnel

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: mercur-e-bot
credentials-file: /home/user/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: bot.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

### 5. Run Tunnel

```bash
cloudflared tunnel run mercur-e-bot
```

## Manual API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "github_app_id": 123456,
  "fastmcp_enabled": true,
  "pam_enabled": false
}
```

### Parse Comment API

```bash
curl -X POST http://localhost:8000/api/parse-comment \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "/test ci.yml\n/merge squash\n/report"
  }'
```

Expected response:
```json
{
  "success": true,
  "commands": [
    {"command": "test", "args": "ci.yml"},
    {"command": "merge", "args": "squash"},
    {"command": "report", "args": ""}
  ],
  "count": 3
}
```

### Status API

```bash
curl http://localhost:8000/api/status
```

## Testing Webhook Signature Validation

### Generate Test Signature

```python
import hmac
import hashlib

payload = b'{"action": "created"}'
secret = b'your_webhook_secret'

signature = 'sha256=' + hmac.new(secret, payload, hashlib.sha256).hexdigest()
print(signature)
```

### Send Test Webhook

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -H "X-Hub-Signature-256: sha256=<calculated_signature>" \
  -d '{"action": "created"}'
```

## Testing FastMCP Integration

### 1. Start MCP Server

```bash
# Terminal 3
./run_mcp.sh
```

### 2. Test MCP Tools

```bash
# Install MCP client (if needed)
pip install mcp

# Test parse command
curl -X POST http://localhost:8001/tools/parse_github_comment \
  -H "Content-Type: application/json" \
  -d '{
    "comment_text": "/test workflow.yml"
  }'
```

### 3. Test with AI Assistant

Configure your AI assistant to use MCP server at `http://localhost:8001`

Example prompts:
- "Parse this GitHub comment: /test ci.yml"
- "Analyze pull request #123 in owner/repo"
- "Suggest a command for merging a PR with passing CI"

## Integration Testing

### Test Full Workflow

1. **Create Test Repository**
   - Create a new repository
   - Install your GitHub App
   - Add a simple workflow file

2. **Create Pull Request**
   ```bash
   git checkout -b test-branch
   echo "test" > test.txt
   git add test.txt
   git commit -m "Test commit"
   git push origin test-branch
   ```

3. **Test Commands**
   - Comment `/test` - should trigger workflow
   - Comment `/report` - should post status
   - Comment `/merge squash` - should merge PR

4. **Verify Results**
   - Check GitHub Actions for triggered workflow
   - Check PR comments for bot responses
   - Check PR merge status

## Debugging

### Enable Debug Logging

Edit `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

Restart the bot.

### View Detailed Logs

```bash
# Real-time logs
tail -f logs/githubbot.log

# Search for errors
grep ERROR logs/githubbot.log

# Search for specific event
grep "issue_comment" logs/githubbot.log
```

### Check GitHub Webhook Deliveries

1. Go to GitHub App settings
2. Click "Advanced" → "Recent Deliveries"
3. View request/response for each webhook
4. Redeliver failed webhooks

### Common Issues

#### Webhook signature validation fails
- Check `GITHUB_WEBHOOK_SECRET` matches GitHub App settings
- Verify webhook is using SHA-256 signature
- Check for trailing whitespace in secret

#### Commands not executing
- Verify bot has correct permissions
- Check installation on repository
- Review command syntax (must start with `/`)

#### Authentication errors
- Verify `GITHUB_APP_ID` is correct
- Check `private-key.pem` is valid
- Ensure app is installed on repository

## Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Results show requests/second, latency, etc.
```

### Stress Testing

```bash
# Install wrk
sudo apt install wrk

# Run stress test
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## Security Testing

### Test Webhook Signature Bypass

Try sending webhook without signature:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"action": "created"}'
```

Should return 401 Unauthorized.

### Test Invalid Signature

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -H "X-Hub-Signature-256: sha256=invalid" \
  -d '{"action": "created"}'
```

Should return 401 Unauthorized.

### Test HTTPS Redirect

```bash
# Should redirect to HTTPS
curl -I http://bot.yourdomain.com
```

## Automated Testing (Future)

### Unit Tests

Create `tests/test_commands.py`:

```python
import pytest
from commands import CommandParser

def test_parse_single_command():
    text = "/test ci.yml"
    commands = CommandParser.parse_commands(text)
    assert len(commands) == 1
    assert commands[0]['command'] == 'test'
    assert commands[0]['args'] == 'ci.yml'

def test_parse_multiple_commands():
    text = "/test\n/merge squash\n/report"
    commands = CommandParser.parse_commands(text)
    assert len(commands) == 3
```

Run tests:
```bash
pytest tests/ -v
```

## Monitoring in Production

### Set Up Health Check Monitoring

Use services like:
- UptimeRobot
- Pingdom
- StatusCake

Monitor: `https://bot.yourdomain.com/health`

### Log Monitoring

Use tools like:
- Grafana + Loki
- ELK Stack
- Datadog

### Metrics

Track:
- Webhook processing time
- Command execution success rate
- API response times
- Error rates

---

Happy Testing! 🧪
