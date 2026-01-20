import discord
from discord.ext import commands, tasks
import random
import copy
import os
import json

# ================== ENV ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN")

DATA_FILE = "config.json"
INTERVAL_MINUTES = 5

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== LOAD / SAVE ==================
def load_config():
    if not os.path.exists(DATA_FILE):
        return {
            "channel_id": 0,
            "auto_dao": True
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

config = load_config()

# ================== ĐẠO LÝ THẦY TU ==================
DAO_LY_GOC = [
    "🙏 Tu hành không phải để hơn thua, mà để bớt ngu vì tin người.",
    "🧘 Tâm không tịnh vì còn đọc tin nhắn cũ.",
    "📿 Công đức không sinh ra từ debate lúc 3h sáng.",
    "😌 Bớt sân si thì đời bớt lag.",
    "🍃 Đời vô thường, hôm nay còn onl mai seen.",
    "😈 Phật độ người hữu duyên, admin độ người biết im.",
    "🪷 Tu mà còn cay thì là tu hú.",
    "📵 Tắt Discord không làm tâm an, bật lên là tâm loạn.",
    "🧠 Người tu không sợ thiếu công đức, chỉ sợ thiếu ngủ.",
    "🪔 Khẩu nghiệp nhiều thì tụng bao nhiêu cũng lag tâm.",
    "🐧 Thắng tranh luận không bằng thắng trong im lặng.",
    "📿 Tu là sửa mình, không phải sửa người khác.",
    "😆 Drama là thử thách của người tu online.",
    "🍵 Uống trà tĩnh tâm, đọc chat là động tâm.",
    "🧘 Chưa đắc đạo đã đắc tội thì nên logout.",
    "📜 Miệng nói buông bỏ, tay vẫn check thông báo.",
    "🪷 Seen không rep cũng là một loại nghiệp.",
    "📜 Phật tại tâm, admin tại quyền."
]

dao_con_lai = []

def lay_dao():
    global dao_con_lai
    if not dao_con_lai:
        dao_con_lai = copy.deepcopy(DAO_LY_GOC)
        random.shuffle(dao_con_lai)
    return dao_con_lai.pop(0)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"🧘 Thầy Tu online: {bot.user}")
    if not giang_dao.is_running():
        giang_dao.start()

# ================== AUTO GIẢNG ĐẠO ==================
@tasks.loop(minutes=INTERVAL_MINUTES)
async def giang_dao():
    if not config.get("auto_dao", True):
        return

    channel_id = config.get("channel_id", 0)
    if channel_id == 0:
        return

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(lay_dao())

# ================== COMMANDS ==================

@bot.command()
async def dao(ctx):
    """Giảng đạo ngay"""
    await ctx.send(lay_dao())

@bot.command()
async def batdao(ctx):
    config["auto_dao"] = True
    save_config(config)
    await ctx.send("▶️ **Thầy Tu bắt đầu giảng đạo mỗi 5 phút** 🙏")

@bot.command()
async def tatdao(ctx):
    config["auto_dao"] = False
    save_config(config)
    await ctx.send("⏸️ **Thầy Tu nhập định, tạm ngưng giảng đạo** 🧘")

# ======= CHỈ CHO PHÉP !id #channel =======
@bot.command()
@commands.has_permissions(administrator=True)
async def id(ctx, channel: discord.TextChannel = None):
    if channel is None:
        await ctx.send("❌ Dùng đúng cú pháp: `!id #channel`")
        return

    config["channel_id"] = channel.id
    save_config(config)

    await ctx.send(
        f"📿 **Đã set kênh giảng đạo:** {channel.mention}\n"
        f"🆔 `{channel.id}`"
    )

@id.error
async def id_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Chỉ admin mới được dùng lệnh này")

# ================== RUN ==================
bot.run(TOKEN)
import discord
from discord.ext import commands, tasks
import random
import copy
import os
import json

# ================== ENV ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN")

DATA_FILE = "config.json"
INTERVAL_MINUTES = 5

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== LOAD / SAVE ==================
def load_config():
    if not os.path.exists(DATA_FILE):
        return {
            "channel_id": 0,
            "auto_dao": True
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

config = load_config()

# ================== ĐẠO LÝ THẦY TU ==================
DAO_LY_GOC = [
    "🙏 Tu hành không phải để hơn thua, mà để bớt ngu vì tin người.",
    "🧘 Tâm không tịnh vì còn đọc tin nhắn cũ.",
    "📿 Công đức không sinh ra từ debate lúc 3h sáng.",
    "😌 Bớt sân si thì đời bớt lag.",
    "🍃 Đời vô thường, hôm nay còn onl mai seen.",
    "😈 Phật độ người hữu duyên, admin độ người biết im.",
    "🪷 Tu mà còn cay thì là tu hú.",
    "📵 Tắt Discord không làm tâm an, bật lên là tâm loạn.",
    "🧠 Người tu không sợ thiếu công đức, chỉ sợ thiếu ngủ.",
    "🪔 Khẩu nghiệp nhiều thì tụng bao nhiêu cũng lag tâm.",
    "🐧 Thắng tranh luận không bằng thắng trong im lặng.",
    "📿 Tu là sửa mình, không phải sửa người khác.",
    "😆 Drama là thử thách của người tu online.",
    "🍵 Uống trà tĩnh tâm, đọc chat là động tâm.",
    "🧘 Chưa đắc đạo đã đắc tội thì nên logout.",
    "📜 Miệng nói buông bỏ, tay vẫn check thông báo.",
    "🪷 Seen không rep cũng là một loại nghiệp.",
    "📜 Phật tại tâm, admin tại quyền."
]

dao_con_lai = []

def lay_dao():
    global dao_con_lai
    if not dao_con_lai:
        dao_con_lai = copy.deepcopy(DAO_LY_GOC)
        random.shuffle(dao_con_lai)
    return dao_con_lai.pop(0)

# ================== READY ==================
@bot.event
async def on_ready():
    print(f"🧘 Thầy Tu online: {bot.user}")
    if not giang_dao.is_running():
        giang_dao.start()

# ================== AUTO GIẢNG ĐẠO ==================
@tasks.loop(minutes=INTERVAL_MINUTES)
async def giang_dao():
    if not config.get("auto_dao", True):
        return

    channel_id = config.get("channel_id", 0)
    if channel_id == 0:
        return

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(lay_dao())

# ================== COMMANDS ==================

@bot.command()
async def dao(ctx):
    """Giảng đạo ngay"""
    await ctx.send(lay_dao())

@bot.command()
async def batdao(ctx):
    config["auto_dao"] = True
    save_config(config)
    await ctx.send("▶️ **Thầy Tu bắt đầu giảng đạo mỗi 5 phút** 🙏")

@bot.command()
async def tatdao(ctx):
    config["auto_dao"] = False
    save_config(config)
    await ctx.send("⏸️ **Thầy Tu nhập định, tạm ngưng giảng đạo** 🧘")

# ======= CHỈ CHO PHÉP !id #channel =======
@bot.command()
@commands.has_permissions(administrator=True)
async def id(ctx, channel: discord.TextChannel = None):
    if channel is None:
        await ctx.send("❌ Dùng đúng cú pháp: `!id #channel`")
        return

    config["channel_id"] = channel.id
    save_config(config)

    await ctx.send(
        f"📿 **Đã set kênh giảng đạo:** {channel.mention}\n"
        f"🆔 `{channel.id}`"
    )

@id.error
async def id_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Chỉ admin mới được dùng lệnh này")

# ================== RUN ==================
bot.run(TOKEN)
