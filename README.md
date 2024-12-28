# SentinelBot: Smart Server Monitoring & Management

This project provides a Discord bot to monitor server stats and manage VPS servers with reboot buttons for each server. Below is a preview of the bot in action:

## Preview
![Bot Preview]((https://cdn.discordapp.com/attachments/1264840797442932766/1322597852345663579/image.png?ex=677174bc&is=6770233c&hm=45b596fbab684e3b8af3fa9ef265f13af160bc2943a6c64248a47ea43deb2b2d&))

## Features
- Monitors server stats (CPU, Memory, Disk Usage, Uptime, TCP/UDP connections, etc.).
- Consolidates all server information in a single embed message.
- Persistent message ID ensures updates continue across bot restarts.
- Dynamic reboot buttons for each server.

## Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher installed.
- Required Python libraries: `discord`, `paramiko`, `requests`, `python-dotenv`.

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/discord-server-monitor-bot.git
cd discord-server-monitor-bot
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate     # Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure the Environment Variables
Create a `.env` file in the root directory with the following content:

```
# Discord Configuration
BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXX
CHANNEL_ID=XXXXXXXXXXXXXX

# VPS Configuration
VPS_NAMES=VPS1,VPS2
VPS_IPS=XXX.XXX.XXX.XXX,XXX.XXX.XXX.XXX
VPS_USERS=root,root
VPS_PASSWORDS=XXXXXXXXXXXX,XXXXXXXXXXXX

# Panel Configuration
PANEL_URLS=https://vps1.example.com,https://vps2.example.com
PANEL_USERS=admin1,admin2
PANEL_PASSWORDS=XXXXXXXXXXXX,XXXXXXXXXXXX

# Bot Configuration
DELAY=10

```

### 6. Run the Bot
```bash
python bot.py
```

## Platform-Specific Instructions

### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Follow steps 2 to 6 above
```

### Windows
```bash
# Download and install Python from https://www.python.org/downloads/

# Follow steps 2 to 6 above
```

### Mac
```bash
brew install python

# Follow steps 2 to 6 above
```

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the license.

```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
