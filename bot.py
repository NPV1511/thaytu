import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import random
import os

# ================== ENV ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN")

DATA_FILE = "channel.txt"
INTERVAL_MINUTES = 30

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

auto_dao = True

# ================== CHANNEL SAVE ==================
def save_channel(cid: int):
    with open(DATA_FILE, "w") as f:
        f.write(str(cid))

def load_channel():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        return int(f.read().strip())

# ================== LẤY ĐẠO LÝ ONLINE ==================
def get_dao_ly_vn():
    try:
        url = "https://sttchat.vn/stt-dao-ly-cuoc-song/"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        texts = [
            p.text.strip()
            for p in soup.find_all("p")
            if len(p.text.strip()) > 40
        ]

        dao = random.choice(texts)
        return f"🧘 **Thầy Tu giảng đạo:**\n> {dao}"

    except Exception:
        return "🙏 Đạo lý vô thường, mạng lag vẫn phải tu."

# ================== AUTO TASK ==================
@tasks.loop(minutes=INTERVAL_MINUTES)
async def auto_dao_task():
    if not auto_dao:
        return

    cid = load_channel()
    if not cid:
        return

    channel = bot.get_channel(cid)
    if not channel:
        return

    await channel.send(get_dao_ly_vn())

# ================== EVENT ==================
@bot.event
async def on_ready():
    print(f"🧘 Thầy Tu Meme online: {bot.user}")
    if not auto_dao_task.is_running():
        auto_dao_task.start()

# ================== COMMAND ==================
@bot.command()
async def id(ctx, channel: discord.TextChannel):
    save_channel(channel.id)
    await ctx.send(f"✅ Đã set kênh giảng đạo: {channel.mention}")

@bot.command()
async def dao(ctx):
    await ctx.send(get_dao_ly_vn())

@bot.command()
async def batdao(ctx):
    global auto_dao
    auto_dao = True
    await ctx.send("✅ Đã **BẬT** giảng đạo 30 phút/lần")

@bot.command()
async def tatdao(ctx):
    global auto_dao
    auto_dao = False
    await ctx.send("⛔ Đã **TẮT** giảng đạo")

# ================== RUN ==================
bot.run(TOKEN)
