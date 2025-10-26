# ⚡ Quick Start Guide - MERCUR-E GitHub Bot

Get your GitHub bot running in 5 minutes!

## 🎯 Prerequisites

- Python 3.8+
- GitHub App created (name: MERCUR-E)
- Private key downloaded from GitHub App

## 🚀 5-Minute Setup

### Step 1: Setup Environment (1 min)

```bash
cd githubbot
chmod +x setup.sh
./setup.sh
```

### Step 2: Configure (2 min)

```bash
# Edit .env file
nano .env
```

Add your credentials:
```env
GITHUB_APP_ID=123456
GITHUB_WEBHOOK_SECRET=your_secret_here
```

### Step 3: Add Private Key (30 sec)

```bash
# Copy your downloaded private key
cp ~/Downloads/your-app.2024-10-26.private-key.pem ./private-key.pem
chmod 600 private-key.pem
```

### Step 4: Run Locally (30 sec)

```bash
chmod +x run_local.sh
./run_local.sh
```

Bot is now running on `http://localhost:8000`!

### Step 5: Expose with ngrok (1 min)

In a new terminal:

```bash
# Install ngrok from https://ngrok.com/download
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Step 6: Update GitHub App

1. Go to: `https://github.com/settings/apps/MERCUR-E`
2. Update Webhook URL: `https://abc123.ngrok.io/webhook`
3. Save

## ✅ Test It!

1. Install the app on a test repository
2. Create an issue or PR
3. Comment: `/test`
4. Watch the bot respond! 🎉

## 📝 Available Commands

- `/test [workflow]` - Trigger GitHub Actions
- `/merge [method]` - Merge PR (squash/merge/rebase)
- `/report` - Generate status report

## 🆘 Troubleshooting

**Bot not responding?**
- Check ngrok is running
- Verify webhook URL in GitHub App settings
- Check logs: `tail -f logs/githubbot.log`

**Authentication errors?**
- Verify `GITHUB_APP_ID` is correct
- Check `private-key.pem` exists
- Ensure app is installed on repository

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Check [TESTING.md](TESTING.md) for testing guide

---

Need help? Check the logs or create an issue!
