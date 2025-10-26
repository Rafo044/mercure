# 🚀 Deployment Guide for MERCUR-E GitHub Bot

Complete guide for deploying the GitHub bot to production with TLS/HTTPS.

## 📋 Prerequisites

- Ubuntu/Debian server (or similar Linux distribution)
- Domain name pointing to your server
- Root or sudo access
- Docker and Docker Compose installed

## 🖥️ Server Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### 3. Install Nginx (if not using Docker Compose nginx)

```bash
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 4. Install Certbot for Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
```

## 🌐 Domain Configuration

### 1. DNS Setup

Add an A record for your subdomain:

```
Type: A
Name: bot (or your preferred subdomain)
Value: YOUR_SERVER_IP
TTL: 3600
```

Wait for DNS propagation (can take up to 48 hours, usually much faster):

```bash
# Check DNS propagation
nslookup bot.yourdomain.com
```

### 2. Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH

# Enable firewall
sudo ufw enable
sudo ufw status
```

## 📦 Application Deployment

### 1. Clone/Upload Project

```bash
# Create application directory
sudo mkdir -p /opt/mercur-e
sudo chown $USER:$USER /opt/mercur-e

# Upload your project files to /opt/mercur-e
# Or clone from git:
cd /opt/mercur-e
git clone <your-repo-url> .
```

### 2. Configure Environment

```bash
cd /opt/mercur-e

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Update with your production values:

```env
# GitHub App Configuration
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY_PATH=./private-key.pem
GITHUB_WEBHOOK_SECRET=your_secure_webhook_secret

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# PAM Authentication
PAM_SERVICE=login
PAM_ENABLED=False

# AI Integration
FASTMCP_ENABLED=True
FASTMCP_PORT=8001

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/githubbot.log

# Security
ALLOWED_ORIGINS=https://bot.yourdomain.com
```

### 3. Add GitHub App Private Key

```bash
# Upload your private-key.pem file
nano private-key.pem
# Paste your private key content

# Set proper permissions
chmod 600 private-key.pem
```

### 4. Update Nginx Configuration

```bash
# Edit nginx.conf
nano nginx.conf
```

Replace all instances of `your-domain.com` with your actual domain (e.g., `bot.yourdomain.com`).

## 🔒 SSL/TLS Setup

### Method 1: Using Certbot (Recommended)

```bash
# Obtain SSL certificate
sudo certbot --nginx -d bot.yourdomain.com

# Follow the prompts:
# - Enter email address
# - Agree to terms
# - Choose whether to redirect HTTP to HTTPS (recommended: yes)
```

Certbot will automatically:
- Obtain certificate from Let's Encrypt
- Configure Nginx
- Set up auto-renewal

### Method 2: Manual Certificate

If using Docker Compose with included nginx:

```bash
# Obtain certificate only (without nginx auto-config)
sudo certbot certonly --standalone -d bot.yourdomain.com

# Certificates will be saved to:
# /etc/letsencrypt/live/bot.yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/bot.yourdomain.com/privkey.pem
```

Update `docker-compose.yml` to mount certificates:

```yaml
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

### 3. Test Auto-Renewal

```bash
# Dry run renewal
sudo certbot renew --dry-run

# If successful, certbot will auto-renew before expiration
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
cd /opt/mercur-e

# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Docker Only

```bash
# Build image
docker build -t mercur-e .

# Run container
docker run -d \
  --name mercur-e \
  --restart unless-stopped \
  -p 8000:8000 \
  -p 8001:8001 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/private-key.pem:/app/private-key.pem:ro \
  --env-file .env \
  mercur-e

# Check logs
docker logs -f mercur-e
```

## 🔧 Nginx Configuration (Standalone)

If not using Docker Compose nginx:

```bash
# Create nginx site configuration
sudo nano /etc/nginx/sites-available/mercur-e
```

Add configuration:

```nginx
upstream githubbot {
    server localhost:8000;
}

server {
    listen 80;
    server_name bot.yourdomain.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name bot.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/bot.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    location /webhook {
        proxy_pass http://githubbot;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        proxy_pass http://githubbot;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/mercur-e /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## 🔄 GitHub App Configuration

### 1. Update Webhook URL

Go to your GitHub App settings:

```
https://github.com/settings/apps/MERCUR-E
```

Update webhook URL:
```
https://bot.yourdomain.com/webhook
```

### 2. Verify Webhook Secret

Ensure the webhook secret in GitHub matches your `.env` file.

### 3. Test Webhook

GitHub provides a "Recent Deliveries" section where you can:
- View webhook payloads
- Redeliver webhooks
- Check response status

## ✅ Verification

### 1. Health Check

```bash
# Local
curl http://localhost:8000/health

# Public
curl https://bot.yourdomain.com/health
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

### 2. Test Webhook

Create a test issue or PR comment with `/test` in a repository where the app is installed.

Check logs:
```bash
# Docker Compose
docker-compose logs -f githubbot

# Docker
docker logs -f mercur-e

# Local logs
tail -f /opt/mercur-e/logs/githubbot.log
```

### 3. SSL Check

```bash
# Check SSL certificate
openssl s_client -connect bot.yourdomain.com:443 -servername bot.yourdomain.com

# Or use online tools:
# https://www.ssllabs.com/ssltest/
```

## 📊 Monitoring

### 1. Set Up Log Rotation

```bash
sudo nano /etc/logrotate.d/mercur-e
```

Add:
```
/opt/mercur-e/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### 2. Monitor with systemd (Alternative to Docker)

Create systemd service:

```bash
sudo nano /etc/systemd/system/mercur-e.service
```

```ini
[Unit]
Description=MERCUR-E GitHub Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mercur-e
Environment="PATH=/opt/mercur-e/venv/bin"
ExecStart=/opt/mercur-e/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mercur-e
sudo systemctl start mercur-e
sudo systemctl status mercur-e
```

## 🔄 Updates and Maintenance

### Update Application

```bash
cd /opt/mercur-e

# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Backup

```bash
# Backup configuration and keys
tar -czf mercur-e-backup-$(date +%Y%m%d).tar.gz \
  .env \
  private-key.pem \
  logs/

# Store backup securely
```

### Certificate Renewal

Certbot auto-renews, but you can manually renew:

```bash
sudo certbot renew
sudo systemctl reload nginx
```

## 🐛 Troubleshooting

### Webhook not working

1. Check firewall allows port 443
2. Verify DNS points to correct IP
3. Check nginx is running: `sudo systemctl status nginx`
4. Review nginx logs: `sudo tail -f /var/log/nginx/error.log`
5. Check application logs: `docker-compose logs -f`

### SSL certificate issues

```bash
# Check certificate validity
sudo certbot certificates

# Renew if needed
sudo certbot renew --force-renewal
```

### Application crashes

```bash
# Check logs
docker-compose logs --tail=100 githubbot

# Restart services
docker-compose restart

# Check resource usage
docker stats
```

## 📈 Performance Optimization

### 1. Enable HTTP/2

Already enabled in nginx configuration.

### 2. Add Caching Headers

Update nginx configuration to add caching for static assets.

### 3. Rate Limiting

Already configured in `nginx.conf` for webhook endpoint.

### 4. Resource Limits

Update `docker-compose.yml`:

```yaml
services:
  githubbot:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 🎯 Production Checklist

- [ ] Domain DNS configured
- [ ] SSL certificate obtained and valid
- [ ] `.env` file configured with production values
- [ ] `private-key.pem` uploaded and secured (chmod 600)
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] Nginx configured and running
- [ ] Docker containers running
- [ ] GitHub App webhook URL updated
- [ ] Webhook deliveries successful
- [ ] Health check endpoint responding
- [ ] Logs being written correctly
- [ ] Log rotation configured
- [ ] Backup strategy in place
- [ ] Monitoring set up

---

Your MERCUR-E GitHub Bot should now be running securely in production! 🎉
