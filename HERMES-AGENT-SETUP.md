# Hermes Agent Setup Guide

Hermes Agent is an autonomous AI agent by Nous Research that lives on your server, remembers what it learns, and gets more capable over time. It supports Telegram, Discord, Slack, WhatsApp, and CLI access.

> Similar to OpenClaw but with persistent memory, auto-generated skills, 40+ built-in tools, and multi-platform messaging gateway.

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
```

This installs Python 3.11, Node.js 22, uv, and clones the repo to `~/.hermes/hermes-agent/`.

**Requirements:** Linux, macOS, or WSL2. Git and curl must be available.

## Initial Setup

```bash
# 1. Run the setup wizard (connects to Nous Portal / OpenRouter / custom endpoint)
hermes setup

# 2. Choose your model
hermes model

# 3. Start the CLI
hermes
```

## Directory Structure

After install, everything lives in `~/.hermes/`:

```
~/.hermes/
├── config.yaml          # Main settings (model, terminal, TTS, etc.)
├── .env                 # API keys and secrets
├── auth.json            # OAuth credentials
├── SOUL.md              # Agent identity/persona
├── memories/            # Persistent memory files
├── skills/              # Agent-created skills
├── cron/                # Scheduled jobs
├── sessions/            # Gateway sessions
└── logs/                # Error and gateway logs
```

## Telegram Bot Setup

### Step 1: Create a Bot with BotFather

1. Open Telegram, search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Provide a display name (e.g. "Hermes Agent")
4. Provide a unique username ending in `bot` (e.g. `my_hermes_bot`)
5. BotFather gives you a token like: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`

### Step 2: Get Your Telegram User ID

Message [@userinfobot](https://t.me/userinfobot) or [@get_id_bot](https://t.me/get_id_bot) to find your numeric user ID (e.g. `123456789`).

### Step 3: Configure Hermes

**Option A — Interactive (recommended):**

```bash
hermes gateway setup
# Select Telegram, paste your bot token and user ID
```

**Option B — Manual:**

Add to `~/.hermes/.env`:

```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_ALLOWED_USERS=123456789
# For multiple users: TELEGRAM_ALLOWED_USERS=123456789,987654321
```

### Step 4: Group Chat Privacy (Optional)

If using the bot in group chats:

1. Message @BotFather → `/mybots` → Select your bot
2. **Bot Settings → Group Privacy → Turn off**
3. **Remove and re-add** the bot to groups (Telegram caches privacy state)

Or simply promote the bot to group admin (admins always see all messages).

### Step 5: Set Home Channel for Scheduled Tasks (Optional)

In any Telegram chat, send `/sethome` to set it as the destination for cron/scheduled task output.

Or manually in `~/.hermes/.env`:

```env
TELEGRAM_HOME_CHANNEL=-1001234567890
# Group IDs are negative; personal DMs use your user ID
```

## Server Deployment

### Deploy on a VPS

Works on any Linux server ($5 VPS is fine):

```bash
# SSH into your server
ssh user@your-server-ip

# Install Hermes
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc

# Run setup
hermes setup
hermes model

# Configure Telegram (see above)
hermes gateway setup
```

### Run as systemd Service (Recommended for Production)

This keeps Hermes running 24/7 and auto-restarts on failure:

```bash
# Install as systemd service
hermes gateway install

# Or manually create the service:
sudo tee /etc/systemd/system/hermes-agent.service > /dev/null <<'EOF'
[Unit]
Description=Hermes Agent Gateway
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username
ExecStart=/home/your-username/.local/bin/hermes gateway
Restart=always
RestartSec=10
Environment=HOME=/home/your-username

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hermes-agent
sudo systemctl start hermes-agent
```

### Check Status

```bash
sudo systemctl status hermes-agent
journalctl -u hermes-agent -f  # Follow logs
```

### Terminal Backend Options

Configure in `~/.hermes/config.yaml`:

```yaml
# Local (default, no isolation)
terminal:
  backend: local

# Docker (sandboxed)
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"

# SSH (run commands on remote server)
terminal:
  backend: ssh
# + set TERMINAL_SSH_HOST, TERMINAL_SSH_USER in .env

# Modal (serverless, cost-effective hibernation)
terminal:
  backend: modal
# + set MODAL_TOKEN_ID, MODAL_TOKEN_SECRET in .env
```

## Key Configuration

### Model Provider (`~/.hermes/.env`)

```env
# Nous Portal (OAuth via hermes setup)
# OpenRouter (200+ models)
OPENROUTER_API_KEY=sk-or-...

# Or custom endpoint
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=http://localhost:1234/v1
```

### Agent Settings (`~/.hermes/config.yaml`)

```yaml
agent:
  max_turns: 90
  reasoning_effort: ""  # xhigh|high|low|minimal|none

memory:
  memory_enabled: true
  user_profile_enabled: true

compression:
  enabled: true
  threshold: 0.50

approvals:
  mode: manual  # manual|smart|off

display:
  streaming: false
  show_reasoning: false
```

## Useful Commands

```bash
hermes              # Start CLI
hermes gateway      # Start messaging gateway (Telegram, Discord, etc.)
hermes gateway setup  # Configure platforms
hermes gateway install  # Install as systemd service
hermes model        # Change model
hermes tools        # Enable/disable tools
hermes update       # Update to latest version
hermes doctor       # Diagnose issues
hermes config       # View config
hermes config edit  # Edit config.yaml
```

## Migrating from OpenClaw

```bash
hermes claw migrate              # Interactive full import
hermes claw migrate --dry-run    # Preview changes
hermes claw migrate --preset user-data  # Skip API secrets
```

Imports persona (SOUL.md), memories, skills, command allowlists, messaging configs, and API keys.

## Resources

- **Website:** https://hermes-agent.nousresearch.com
- **GitHub:** https://github.com/NousResearch/hermes-agent
- **Docs:** https://hermes-agent.nousresearch.com/docs
- **Discord:** https://discord.gg/NousResearch
- **Nous Portal:** https://portal.nousresearch.com
