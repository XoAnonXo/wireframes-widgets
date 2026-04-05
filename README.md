# HermesAgentAnonSetup

Setup guide and scripts for deploying [Hermes Agent](https://hermes-agent.nousresearch.com) by Nous Research — an autonomous AI agent that lives on your server, remembers what it learns, and connects to Telegram, Discord, Slack, and more.

## Quick Start

```bash
# One-liner install
bash scripts/setup-hermes.sh
```

Or step by step:

```bash
# 1. Install Hermes Agent
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc

# 2. Setup wizard (LLM provider, API keys)
hermes setup

# 3. Connect Telegram
hermes gateway setup

# 4. Run 24/7 as a service
hermes gateway install
```

## What's in This Repo

| File | Description |
|------|-------------|
| `HERMES-AGENT-SETUP.md` | Full setup guide — install, Telegram bot, server deploy, systemd, config reference |
| `scripts/setup-hermes.sh` | Interactive install + setup script |

## What is Hermes Agent?

- Autonomous agent that runs on your server (even a $5 VPS)
- Persistent memory — learns and improves over time
- 40+ built-in tools (web search, terminal, browser, vision, code exec)
- Multi-platform: Telegram, Discord, Slack, WhatsApp, Signal, Email, CLI
- Scheduled tasks, subagent delegation, sandboxed execution
- MIT licensed, by [Nous Research](https://nousresearch.com)

## Resources

- [Hermes Agent Website](https://hermes-agent.nousresearch.com)
- [GitHub Repo](https://github.com/NousResearch/hermes-agent)
- [Documentation](https://hermes-agent.nousresearch.com/docs)
- [Nous Research Discord](https://discord.gg/NousResearch)
