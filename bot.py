import discord
from discord.ext import commands
from discord import app_commands
import json
import os

TOKEN = os.getenv("TOKEN")  # Railway sẽ đọc biến môi trường

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "config.json"

# ================= LOAD / SAVE =================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot đã online: {bot.user}")

# ================= SET ROLE =================
@bot.tree.command(name="role", description="Set role cần theo dõi")
@app_commands.checks.has_permissions(administrator=True)
async def set_role(interaction: discord.Interaction, role: discord.Role):
    guild_id = str(interaction.guild.id)

    if guild_id not in data:
        data[guild_id] = {}

    data[guild_id]["role"] = role.id
    save_data(data)

    await interaction.response.send_message(
        f"✅ Đã set role: {role.mention}", ephemeral=True
    )

# ================= SET CHANNEL =================
@bot.tree.command(name="channel", description="Set kênh thông báo")
@app_commands.checks.has_permissions(administrator=True)
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = str(interaction.guild.id)

    if guild_id not in data:
        data[guild_id] = {}

    data[guild_id]["channel"] = channel.id
    save_data(data)

    await interaction.response.send_message(
        f"✅ Đã set channel: {channel.mention}", ephemeral=True
    )

# ================= ROLE UPDATE =================
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    guild_id = str(after.guild.id)

    if guild_id not in data:
        return

    role_id = data[guild_id].get("role")
    channel_id = data[guild_id].get("channel")

    if not role_id or not channel_id:
        return

    role = after.guild.get_role(role_id)
    channel = after.guild.get_channel(channel_id)

    if not role or not channel:
        return

    if role not in before.roles and role in after.roles:
        await channel.send(
            f"{after.mention} Đã Được Duyệt Vui Lòng Đọc Kĩ nội Dung Ở Phần <#1461276993126662299> Và Làm Theo Để Được Phỏng Vấn <3"
        )

# ================= RUN =================
bot.run(TOKEN)
