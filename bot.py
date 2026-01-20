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

# ================== TIỆN ÍCH ==================
def save_channel(cid: int):
    with open(DATA_FILE, "w") as f:
        f.write(str(cid))

def load_channel():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        return int(f.read().strip())

# ================== LẤY ĐẠO LÝ MEME ==================
def get_dao_ly_vn():
    try:
        url = "https://sttchat.vn/stt-dao-ly-cuoc-song/"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        items = soup.find_all("p")
        texts = [i.text.strip() for i in items if len(i.text.strip()) > 40]

        meme = random.choice(texts)
        return f"🧘 **Thầy Tu giảng đạo:**\n> {meme}"
    except:
        return "🙏 Tu hành gặp lỗi mạng, tâm vẫn phải tịnh."

# ================== ẢNH MEME ==================
def get_meme_image():
    return random.choice([
        "https://i.imgur.com/9YQZ0YQ.jpg",
        "https://i.imgur.com/6XGQH7m.jpg",
        "https://i.imgur.com/Z7AzH2c.jpg",
        "https://i.imgur.com/0y8Ftya.jpg"
    ])

# ================== TASK TỰ ĐỘNG ==================
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

    embed = discord.Embed(
        description=get_dao_ly_vn(),
        color=0xFFD966
    )
    embed.set_image(url=get_meme_image())
    await channel.send(embed=embed)

# ================== EVENT ==================
@bot.event
async def on_ready():
    print(f"🧘 Thầy Tu Meme online: {bot.user}")
    if not auto_dao_task.is_running():
        auto_dao_task.start()

# ================== LỆNH ==================
@bot.command()
async def id(ctx, channel: discord.TextChannel):
    save_channel(channel.id)
    await ctx.send(f"✅ Đã set kênh giảng đạo: {channel.mention}")

@bot.command()
async def dao(ctx):
    embed = discord.Embed(
        description=get_dao_ly_vn(),
        color=0xFFD966
    )
    embed.set_image(url=get_meme_image())
    await ctx.send(embed=embed)

@bot.command()
async def batdao(ctx):
    global auto_dao
    auto_dao = True
    await ctx.send("✅ Đã **BẬT** chế độ giảng đạo 30 phút/lần")

@bot.command()
async def tatdao(ctx):
    global auto_dao
    auto_dao = False
    await ctx.send("⛔ Đã **TẮT** chế độ giảng đạo")

# ================== RUN ==================
bot.run(TOKEN)
