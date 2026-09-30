# SentinelBot

Discord bot for monitoring VPS and 3x-ui panel status from one persistent Discord message.

The bot collects server metrics, panel usage data, and uptime information, then updates a Discord embed with control buttons for common server actions.

## Features

- CPU, memory, disk, uptime, TCP/UDP, and network usage summaries
- Multi-server configuration through environment variables
- 3x-ui panel login and usage collection
- Persistent Discord status message across bot restarts
- Server action buttons for operational workflows

## Requirements

- Python 3.9+
- Discord bot token
- SSH access or panel credentials for the servers you want to monitor

Install dependencies:

```bash
pip install discord.py paramiko requests python-dotenv
```

## Configuration

Create a `.env` file:

```properties
BOT_TOKEN=your_discord_bot_token
CHANNEL_ID=your_discord_channel_id

VPS_NAMES=VPS1,VPS2
VPS_IPS=203.0.113.10,203.0.113.11
VPS_USERS=root,root
VPS_PASSWORDS=password1,password2

PANEL_URLS=https://panel1.example.com,https://panel2.example.com
PANEL_USERS=admin1,admin2
PANEL_PASSWORDS=password1,password2

DELAY=10
```

Do not commit real tokens, passwords, or server credentials.

## Running

```bash
python main.py
```

## Notes

This project is intended for private server operations. Use least-privilege credentials, private Discord channels, and a safe hosting environment.
