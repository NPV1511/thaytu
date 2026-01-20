import discord
from discord.ext import commands, tasks
import os
import json
import random
import requests
from bs4 import BeautifulSoup

# ================== ENV ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN")

DATA_FILE = "config.json"
CACHE_FILE = "cache.json"
INTERVAL_MINUTES = 30

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== LOAD / SAVE ==================
def load_json(path, default):
    if not os.path.exists(path):
        return default
    return json.load(open(path, "r", encoding="utf-8"))

def save_json(path, data):
    json.dump(data, open(path, "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

config = load_json(DATA_FILE, {"channel_id": 0, "auto": True})
cache = load_json(CACHE_FILE, {"texts": [], "images": []})

# ================== CHẾ ĐẠO LÝ TIẾNG VIỆT ==================
VIET_PREFIX = [
    "🧘 Thầy tu nói:",
    "📿 Đạo lý online:",
    "🍃 Ngẫm mà xem:",
    "😌 Tu rồi mới hiểu:",
    "🙏 Phật dạy (phiên bản Discord):",
    "🪷 Một phút tĩnh tâm:",
]

VIET_ENDING = [
    "…ngẫm đi rồi hẵng cãi.",
    "— tu chưa tới thì đừng cay.",
    "— đọc xong nhớ thở.",
    "— ai hiểu thì hiểu.",
    "— không hợp thì lướt.",
    "— đạo tới đây thôi."
]

def viet_hoa_dao(eng_text: str):
    """
    Không dịch word-by-word.
    Chế lại thành meme tiếng Việt cho hợp Discord.
    """
    eng_text = eng_text.strip()

    # rút gọn cho hợp meme
    if len(eng_text) > 120:
        eng_text = eng_text[:120] + "..."

    prefix = random.choice(VIET_PREFIX)
    ending = random.choice(VIET_ENDING)

    return f"{prefix}\n**{eng_text}**\n{ending}"

# ================== FETCH ĐẠO LÝ GỐC ==================
def fetch_texts():
    url = "https://www.goodreads.com/quotes/tag/philosophy"
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    texts = []
    for q in soup.select(".quoteText"):
        t = q.get_text(strip=True).split("―")[0]
        if len(t) > 40:
            texts.append(viet_hoa_dao(t))

    random.shuffle(texts)
    return texts

# ================== FETCH ẢNH MEME ==================
def fetch_images():
    subs = ["memes", "wholesomememes", "buddhism", "philosophy"]
    images = []

    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/top.json?limit=25&t=day"
        headers = {"User-Agent": "thay-tu-meme-bot"}
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            continue

        for post in res.json()["data"]["children"]:
            img = post["data"].get("url_overridden_by_dest", "")
            if img.endswith((".jpg", ".png", ".jpeg")):
                images.append(img)

    random.shuffle(images)
    return images

# ================== GET MEME ==================
def get_meme():
    if not cache["texts"]:
        cache["texts"] = fetch_texts()

    if not cache["images"]:
        cache["images"] = fetch_images()

    text = cache["texts"].pop(0)
    image = cache["images"].pop(0)

    save_json(CACHE_FILE, cache)
    return text, image

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"🧘 Thầy Tu Meme online: {bot.user}")
    if not giang_dao.is_running():
        giang_dao.start()

# ================== AUTO GIẢNG ĐẠO ==================
@tasks.loop(minutes=INTERVAL_MINUTES)
async def giang_dao():
    if not config.get("auto", True):
        return

    channel_id = config.get("channel_id", 0)
    if channel_id == 0:
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        return

    text, image = get_meme()
    embed = discord.Embed(description=text, color=0x9bcb9b)
    embed.set_image(url=image)

    await channel.send(embed=embed)

# ================== COMMANDS ==================
@bot.command()
async def dao(ctx):
    text, image = get_meme()
    embed = discord.Embed(description=text, color=0x9bcb9b)
    embed.set_image(url=image)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def id(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send("❌ Dùng đúng: `!id #channel`")
        return

    config["channel_id"] = channel.id
    save_json(DATA_FILE, config)
    await ctx.send(f"📿 Đã set kênh giảng đạo: {channel.mention}")

@bot.command()
async def tatdao(ctx):
    config["auto"] = False
    save_json(DATA_FILE, config)
    await ctx.send("⏸️ Thầy Tu nhập định")

@bot.command()
async def batdao(ctx):
    config["auto"] = True
    save_json(DATA_FILE, config)
    await ctx.send("▶️ Thầy Tu tiếp tục giảng đạo")

# ================== RUN ==================
bot.run(TOKEN)
