import discord
from discord import ButtonStyle, ui, Embed
import os
from dotenv import load_dotenv
import asyncio
import requests
import paramiko
import logging
import json
from datetime import timedelta

# -------------------- Configuration --------------------
load_dotenv()  # Load environment variables from .env

# Setup Logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO for minimal logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Fetch Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
VPS_NAMES = os.getenv("VPS_NAMES", "").split(",")
VPS_IPS = os.getenv("VPS_IPS", "").split(",")
VPS_USERS = os.getenv("VPS_USERS", "").split(",")
VPS_PASSWORDS = os.getenv("VPS_PASSWORDS", "").split(",")
PANEL_URLS = os.getenv("PANEL_URLS", "").split(",")
PANEL_USERS = os.getenv("PANEL_USERS", "").split(",")
PANEL_PASSWORDS = os.getenv("PANEL_PASSWORDS", "").split(",")
DELAY = int(os.getenv("DELAY", "5"))

MESSAGE_TRACKER_FILE = "message_tracker.json"

# Ensure Environment Variables are Correct
if not (BOT_TOKEN and CHANNEL_ID and VPS_NAMES and VPS_IPS and VPS_USERS and VPS_PASSWORDS and PANEL_URLS):
    logging.error("One or more required environment variables are missing.")
    exit(1)

if len(VPS_NAMES) != len(VPS_IPS) or len(VPS_NAMES) != len(VPS_USERS) or len(VPS_NAMES) != len(VPS_PASSWORDS):
    logging.error("VPS details in environment variables are misaligned.")
    exit(1)

# Cache for session cookies
session_cookies = {}

# -------------------- Utility Functions --------------------
def load_message_id():
    """Load the saved message ID from file."""
    if os.path.exists(MESSAGE_TRACKER_FILE):
        with open(MESSAGE_TRACKER_FILE, "r") as f:
            data = json.load(f)
            return data.get("message_id")
    return None

def save_message_id(message_id):
    """Save the message ID to file."""
    with open(MESSAGE_TRACKER_FILE, "w") as f:
        json.dump({"message_id": message_id}, f)

def login_to_panel(panel_url, username, password):
    """Logs into the panel and retrieves a session cookie."""
    login_url = f"{panel_url}/login"
    payload = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(login_url, data=payload, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("success"):
                session_cookie = response.cookies.get("3x-ui")
                return session_cookie
        logging.error(f"Login failed for panel: {panel_url}")
    except Exception as e:
        logging.error(f"Error logging into panel: {e}")
    return None

def collect_usage_from_panel(panel_url, session_cookie):
    """Collects usage stats from the panel API."""
    status_url = f"{panel_url}/server/status"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*'
    }
    cookies = {
        '3x-ui': session_cookie
    }
    try:
        response = requests.post(status_url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("success"):
                return json_data.get("obj", {})
        logging.warning(f"Failed to fetch panel data from {panel_url}")
    except Exception as e:
        logging.error(f"Error fetching data from panel: {e}")
    return {}

def reboot_vps(vps_ip, user, password):
    """Reboots the VPS via SSH."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_ip, username=user, password=password)
        ssh.exec_command("sudo reboot")
        ssh.close()
        return "Reboot command sent successfully."
    except Exception as e:
        logging.error(f"Error rebooting VPS {vps_ip}: {e}")
        return f"Error: {e}"

def format_uptime(seconds):
    """Formats uptime as days, hours, minutes, and seconds."""
    try:
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{days}d {hours}h {minutes}m {seconds}s"
    except Exception as e:
        logging.error(f"Error formatting uptime: {e}")
        return "N/A"

# -------------------- Discord Bot Setup --------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class ServerControlView(ui.View):
    def __init__(self, vps_data):
        super().__init__(timeout=None)
        for vps_name, vps_ip, user, password in vps_data:
            self.add_item(RebootButton(vps_name, vps_ip, user, password))

class RebootButton(ui.Button):
    def __init__(self, vps_name, vps_ip, user, password):
        super().__init__(label=f"Reboot {vps_name}", style=ButtonStyle.danger)
        self.vps_name = vps_name
        self.vps_ip = vps_ip
        self.user = user
        self.password = password

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        result = reboot_vps(self.vps_ip, self.user, self.password)
        await interaction.followup.send(f"Rebooting **{self.vps_name}**: {result}", ephemeral=True)

async def update_status_message(channel):
    """Continuously update the status message in the specified channel."""
    message_id = load_message_id()
    status_message = None

    if message_id:
        try:
            status_message = await channel.fetch_message(message_id)
        except discord.NotFound:
            pass

    while True:
        embed = Embed(title="Server Monitoring", color=discord.Color.green())
        vps_data = []
        for name, ip, user, password, panel_url, panel_user, panel_pass in zip(
            VPS_NAMES, VPS_IPS, VPS_USERS, VPS_PASSWORDS, PANEL_URLS, PANEL_USERS, PANEL_PASSWORDS
        ):
            # Ensure session cookie exists
            if panel_url not in session_cookies:
                session_cookie = login_to_panel(panel_url, panel_user, panel_pass)
                if session_cookie:
                    session_cookies[panel_url] = session_cookie
                else:
                    continue

            # Collect usage stats from the panel
            usage = collect_usage_from_panel(panel_url, session_cookies[panel_url])
            if not usage:
                continue

            # Format uptime
            uptime_str = format_uptime(usage.get("uptime", 0))

            # Calculate total bandwidth usage
            sent_bandwidth = usage["netTraffic"]["sent"] / (1024 * 1024 * 1024)
            recv_bandwidth = usage["netTraffic"]["recv"] / (1024 * 1024 * 1024)
            total_bandwidth_gb = (sent_bandwidth + recv_bandwidth)

            # Add fields for this server
            embed.add_field(
                name=f"Server: {name}",
                value=(
                    f"**IP Address:** {ip}\n"
                    f"**CPU Usage:** {usage.get('cpu', 0):.2f}%\n"
                    f"**Memory Usage:** {usage['mem']['current'] / (1024 * 1024):.1f}/{usage['mem']['total'] / (1024 * 1024):.1f} MB\n"
                    f"**Disk Usage:** {usage['disk']['current'] / (1024 * 1024 * 1024):.1f}/{usage['disk']['total'] / (1024 * 1024 * 1024):.1f} GB\n"
                    f"**Uptime:** {uptime_str}\n"
                    f"**TCP Connections:** {usage.get('tcpCount', 'N/A')}\n"
                    f"**UDP Connections:** {usage.get('udpCount', 'N/A')}\n"
                    f"**Network IO (real-time):** TX: {usage['netIO']['up'] / (1024 * 1024):.2f} MB, RX: {usage['netIO']['down'] / (1024 * 1024):.2f} MB\n"
                    f"**Total Bandwidth:** Sent: {sent_bandwidth:.2f} GB, Received: {recv_bandwidth:.2f} GB\n"
                    f"Overall: {total_bandwidth_gb:.2f} GB"
                ),
                inline=False
            )

            # Add to VPS data for control view
            vps_data.append((name, ip, user, password))

        # Update or send the message
        if not status_message:
            status_message = await channel.send(embed=embed, view=ServerControlView(vps_data))
            save_message_id(status_message.id)
        else:
            await status_message.edit(embed=embed, view=ServerControlView(vps_data))

        await asyncio.sleep(DELAY)

@client.event
async def on_ready():
    logging.info(f"Bot logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🤖 Bot is online and monitoring servers!")
        asyncio.create_task(update_status_message(channel))
    else:
        logging.error(f"Channel with ID {CHANNEL_ID} not found.")

# -------------------- Main --------------------
if __name__ == "__main__":
    try:
        client.run(BOT_TOKEN)
    except discord.LoginFailure:
        logging.error("Invalid BOT_TOKEN provided. Please check your .env file.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
