import discord
from discord.ext import commands
from discord import app_commands
import asyncio, random, os, time

# ================== TOKEN ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Chưa set TOKEN trên Railway")

# ================== DAO LY (GIỮ NGUYÊN) ==================
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

# ================== BOT ==================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== DROP VIEW ==================
class DropView(discord.ui.View):
    def __init__(self, gift, duration):
        super().__init__(timeout=duration)
        self.gift = gift
        self.end_time = time.time() + duration
        self.clicked = set()
        self.processing = set()
        self.claimed = False
        self.msg = None
        self.lock = asyncio.Lock()

    def time_left(self):
        left = max(0, int(self.end_time - time.time()))
        if left >= 3600:
            return f"{left//3600}h"
        if left >= 60:
            return f"{left//60}m"
        return f"{left}s"

    def progress_bar(self):
        total = 10
        left = max(0, self.end_time - time.time())
        percent = left / self.timeout
        filled = int(percent * total)
        return "█" * filled + "░" * (total - filled)

    async def on_timeout(self):
        if not self.claimed and self.clicked:
            winner = random.choice(list(self.clicked))
            await self.msg.edit(
                content=f"⏰ **HẾT GIỜ DROP**\n🎉 <@{winner}> nhận **{self.gift}**\n\n📿 {random.choice(DAO_LY)}",
                view=None
            )
        elif not self.clicked:
            await self.msg.edit(content="❌ Drop kết thúc nhưng không ai tham gia.", view=None)

    @discord.ui.button(label="🎁 Nhặt quà", style=discord.ButtonStyle.success)
    async def pick(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = interaction.user.id

        if uid in self.clicked or uid in self.processing:
            await interaction.response.send_message("❌ Bạn đã nhặt rồi!", ephemeral=True)
            return

        self.processing.add(uid)
        await interaction.response.send_message("⏳ Đang nhặt thính...", ephemeral=True)

        async def process():
            async with self.lock:
                await asyncio.sleep(random.randint(1, 3))
                self.processing.discard(uid)
                self.clicked.add(uid)

                if self.claimed:
                    return

                if random.random() <= 0.2:
                    self.claimed = True
                    await self.msg.edit(
                        content=f"🎉 **TRÚNG THƯỞNG** 🎉\n{interaction.user.mention} nhận **{self.gift}**\n\n📿 {random.choice(DAO_LY)}",
                        view=None
                    )
                else:
                    await interaction.followup.send("😢 Nhặt hụt rồi...", ephemeral=True)

        asyncio.create_task(process())

# ================== SLASH COMMAND ==================
@bot.tree.command(name="drop", description="Drop phần quà")
@app_commands.describe(phan_qua="Tên phần quà", time="Thời gian", unit="s / m / h")
async def drop(interaction: discord.Interaction, phan_qua: str, time: int, unit: str):
    if unit not in ["s", "m", "h"]:
        await interaction.response.send_message("❌ unit chỉ s / m / h", ephemeral=True)
        return

    seconds = time * (60 if unit == "m" else 3600 if unit == "h" else 1)
    view = DropView(phan_qua, seconds)

    await interaction.response.send_message(
        f"🎁 **DROP PHẦN QUÀ** 🎁\n🎁 Quà: **{phan_qua}**\n⏳ Time left: {view.time_left()}\n{view.progress_bar()}",
        view=view
    )
    view.msg = await interaction.original_response()

# ================== READY ==================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot online: {bot.user}")

bot.run(TOKEN)
