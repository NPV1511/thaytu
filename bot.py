import discord
from discord.ext import commands, tasks
import os

# ================== ENV ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN")

DATA_FILE = "channel.txt"
INDEX_FILE = "index.txt"
INTERVAL_MINUTES = 30

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

auto_dao = True

# ================== ĐẠO LÝ MẶN SIÊU CẤP ==================
DAO_LY = [
    "😈 Tu rồi mới hiểu: không phải ai im lặng cũng hiền, có người coi bạn không đáng nói.",
    "🧘 Thầy tu không sân si, chỉ là không muốn phí não cho người không hiểu.",
    "😌 Đời dạy ta: càng giải thích, càng giống người sai.",
    "🙃 Không phải mình khó tính, là do tiêu chuẩn mình cao hơn sự vô duyên.",
    "📿 Thấy ai cũng giỏi, trừ lúc làm việc.",
    "🍃 Người khiến bạn mệt thường không đóng góp gì cho cuộc sống bạn.",
    "😈 Trưởng thành là khi đọc tin nhắn mà không còn thấy cần trả lời.",
    "🧠 Khôn không phải nói hay, mà là biết lúc nào nên câm.",
    "🕯️ Im lặng không phải thua, là không thèm chơi.",
    "📵 Online nhiều chỉ làm rõ một điều: ai cũng rảnh miệng.",

    "😌 Thầy tu không ghét ai, chỉ tránh xa cho khỏe.",
    "🙃 Không phải ai cười cũng thân, có người cười vì thấy bạn ngu.",
    "📿 Người làm mình tổn thương thường không nhớ gì về mình.",
    "🍃 Đời không tệ, chỉ là có quá nhiều người không đáng.",
    "😈 Tu giúp ta nhận ra: không ai có nghĩa vụ hiểu mình.",
    "🧠 Biết đủ là giàu, biết né là khôn.",
    "🕯️ Cãi nhau không làm mình đúng hơn, chỉ làm mình xấu đi.",
    "📵 Seen không rep không phải vô lễ, mà là tự trọng.",
    "😌 Đừng cố chứng minh mình đúng với người không biết nghe.",
    "🙃 Nhiều người thích lời thật, nhưng chỉ khi nó không đụng họ.",

    "😈 Thầy tu nhìn thấu nhưng không vạch trần, vì không rảnh.",
    "📿 Không phải ai cũng xứng đáng với sự kiên nhẫn của bạn.",
    "🍃 Buông không phải thua, là không muốn lún sâu.",
    "🧠 Người khôn giữ năng lượng cho bản thân.",
    "😌 Tâm tịnh là khi drama tới mà mình thấy mắc cười.",
    "🙃 Người hay nói đạo lý thường sống khác đạo lý.",
    "🕯️ Đừng buồn vì bị bỏ rơi, có khi là được giải thoát.",
    "📵 Ít nói lại, bạn sẽ ít hối hận hơn.",
    "😈 Thầy tu không block ai, chỉ âm thầm mute.",
    "🧘 Tu là hiểu rằng: không cần ai công nhận.",

    "😌 Không phải ai cũng cần ở lại cuộc đời mình.",
    "🙃 Người không hợp, nói thêm chỉ tốn pin.",
    "📿 Đời đơn giản khi ta bớt kỳ vọng vào người khác.",
    "🍃 Đừng mong người khác hiểu mình, họ còn không hiểu họ.",
    "😈 Im lặng đúng lúc là đỉnh cao của trí tuệ.",
    "🧠 Thắng thua không quan trọng, yên ổn mới đáng tiền.",
    "🕯️ Có những mối quan hệ chỉ nên giữ ở mức… đã từng.",
    "📵 Đôi khi biến mất là cách sống còn.",
    "😌 Tu hành không làm đời đẹp hơn, chỉ làm mình tỉnh hơn.",
    "🧘 Và tỉnh rồi thì… bớt ngu vì người khác."
]

# ================== SAVE / LOAD ==================
def save_channel(cid):
    with open(DATA_FILE, "w") as f:
        f.write(str(cid))

def load_channel():
    if not os.path.exists(DATA_FILE):
        return None
    return int(open(DATA_FILE).read())

def load_index():
    if not os.path.exists(INDEX_FILE):
        return 0
    return int(open(INDEX_FILE).read())

def save_index(i):
    with open(INDEX_FILE, "w") as f:
        f.write(str(i))

def next_dao():
    i = load_index()
    text = DAO_LY[i % len(DAO_LY)]
    save_index(i + 1)
    return text

# ================== AUTO TASK ==================
@tasks.loop(minutes=INTERVAL_MINUTES)
async def auto_dao_task():
    if not auto_dao:
        return

    cid = load_channel()
    if not cid:
        return

    channel = bot.get_channel(cid)
    if channel:
        await channel.send(next_dao())

# ================== EVENT ==================
@bot.event
async def on_ready():
    print(f"😈 Thầy Tu Mặn online: {bot.user}")
    if not auto_dao_task.is_running():
        auto_dao_task.start()

# ================== COMMAND ==================
@bot.command()
async def id(ctx, channel: discord.TextChannel):
    save_channel(channel.id)
    await ctx.send(f"✅ Đã set kênh: {channel.mention}")

@bot.command()
async def dao(ctx):
    await ctx.send(next_dao())

@bot.command()
async def batdao(ctx):
    global auto_dao
    auto_dao = True
    await ctx.send("✅ Đã **BẬT** giảng đạo tự động")

@bot.command()
async def tatdao(ctx):
    global auto_dao
    auto_dao = False
    await ctx.send("⛔ Đã **TẮT** giảng đạo tự động")

# ================== RUN ==================
bot.run(TOKEN)
