#!/usr/bin/env bash
# Hermes Agent quick setup script
# Usage: bash scripts/setup-hermes.sh
set -euo pipefail

echo "========================================="
echo "  Hermes Agent Setup"
echo "========================================="
echo ""

# Check if already installed
if command -v hermes &>/dev/null; then
    echo "[✓] Hermes is already installed: $(which hermes)"
    echo ""
    read -p "Update to latest version? [y/N] " update
    if [[ "$update" =~ ^[Yy]$ ]]; then
        hermes update
    fi
else
    echo "[1/3] Installing Hermes Agent..."
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

    # Source shell profile to get hermes in PATH
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi

    if ! command -v hermes &>/dev/null; then
        export PATH="$HOME/.local/bin:$PATH"
    fi

    echo "[✓] Hermes installed"
fi

echo ""
echo "[2/3] Running setup wizard..."
echo "  This will connect to your LLM provider (Nous Portal, OpenRouter, etc.)"
echo ""
hermes setup

echo ""
echo "[3/3] Setting up Telegram gateway..."
echo ""
echo "  You will need:"
echo "    - A Telegram bot token from @BotFather (/newbot)"
echo "    - Your Telegram user ID from @userinfobot"
echo ""
read -p "Set up Telegram now? [Y/n] " setup_tg
if [[ ! "$setup_tg" =~ ^[Nn]$ ]]; then
    hermes gateway setup
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "  Quick start:"
echo "    hermes              # Start CLI chat"
echo "    hermes gateway      # Start Telegram bot"
echo "    hermes gateway install  # Run as systemd service (24/7)"
echo ""
echo "  Config files: ~/.hermes/"
echo "    .env         - API keys & bot tokens"
echo "    config.yaml  - Settings"
echo "    SOUL.md      - Agent persona"
echo ""
