<!DOCTYPE html>
<html>
<head>
    <title>SentinelBot: Smart Server Monitoring & Management</title>
</head>
<body>
    <h1>SentinelBot: Smart Server Monitoring & Management</h1>

    <p>This project provides a Discord bot to monitor server stats and manage VPS servers with reboot buttons for each server. Below is a preview of the bot in action:</p>

    <h2>Preview</h2>
    <img src="preview.png" alt="Bot Preview">

    <h2>Features</h2>
    <ul>
        <li>Monitors server stats (CPU, Memory, Disk Usage, Uptime, TCP/UDP connections, etc.).</li>
        <li>Consolidates all server information in a single embed message.</li>
        <li>Persistent message ID ensures updates continue across bot restarts.</li>
        <li>Dynamic reboot buttons for each server.</li>
    </ul>

    <h2>Setup Instructions</h2>

    <h3>1. Prerequisites</h3>
    <ul>
        <li>Python 3.9 or higher installed.</li>
        <li>Required Python libraries: <code>discord</code>, <code>paramiko</code>, <code>requests</code>, <code>python-dotenv</code>.</li>
    </ul>

    <h3>2. Clone the Repository</h3>
    <pre>
    git clone https://github.com/yourusername/discord-server-monitor-bot.git
    cd discord-server-monitor-bot
    </pre>

    <h3>3. Create a Virtual Environment</h3>
    <pre>
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate     # Windows
    </pre>

    <h3>4. Install Dependencies</h3>
    <pre>
    pip install -r requirements.txt
    </pre>

    <h3>5. Configure the Environment Variables</h3>
    Create a <code>.env</code> file in the root directory with the following content:

    <pre>
    # Discord Configuration
    BOT_TOKEN=YOUR_BOT_TOKEN
    CHANNEL_ID=DISCORD_CHANNEL_ID

    # VPS Configuration
    VPS_NAMES=SG1,SG2
    VPS_IPS=38.76.247.213,206.189.152.155
    VPS_USERS=root,root
    VPS_PASSWORDS=YourPassword1,YourPassword2

    # Panel Configuration
    PANEL_URLS=https://sg1.example.com,https://sg2.example.com
    PANEL_USERS=admin1,admin2
    PANEL_PASSWORDS=PanelPassword1,PanelPassword2

    # Bot Configuration
    DELAY=10
    </pre>

    <h3>6. Run the Bot</h3>
    <pre>
    python bot.py
    </pre>

    <h2>Platform-Specific Instructions</h2>

    <h3>Linux</h3>
    <pre>
    sudo apt update
    sudo apt install python3 python3-pip python3-venv

    # Follow steps 2 to 6 above
    </pre>

    <h3>Windows</h3>
    <pre>
    # Download and install Python from https://www.python.org/downloads/

    # Follow steps 2 to 6 above
    </pre>

    <h3>Mac</h3>
    <pre>
    brew install python

    # Follow steps 2 to 6 above
    </pre>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the license.</p>

    <pre>
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
    </pre>
</body>
</html>
