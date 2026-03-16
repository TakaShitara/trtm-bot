import discord
from discord.ext import commands
import os
import time

# 修正済み
TOKEN = os.getenv("TRTM_DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("TRTM_DISCORD_TOKEN が設定されていません")

# 修正予定！
TARGET_CHANNEL_ID = 123456789012345678

# 修正済み
GITHUB_PAGES_BASE = "https://takashitara.github.io/trtm-bot/images"

# 修正予定
BUTTONS = [
    {"label": "開始", "image": "start.png"},
    {"label": "終了", "image": "finish.png"},
    {"label": "離席", "image": "afk.png"},
    {"label": "準備OK", "image": "ready.png"},
    {"label": "戻りました", "image": "back.png"},
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


class ReportButton(discord.ui.Button):

    def __init__(self, label, image):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.image = image

    async def callback(self, interaction: discord.Interaction):

        channel = bot.get_channel(TARGET_CHANNEL_ID)

        if channel is None:
            await interaction.response.send_message(
                "送信先チャンネルが見つかりません",
                ephemeral=True
            )
            return

        ts = int(time.time())

        image_url = f"{GITHUB_PAGES_BASE}/{self.image}?ts={ts}"

        embed = discord.Embed()
        embed.set_image(url=image_url)

        await channel.send(embed=embed)

        # ボタン押下のレスポンス（ユーザーには表示されない）
        await interaction.response.defer()


class ReportView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        for btn in BUTTONS:

            self.add_item(
                ReportButton(btn["label"], btn["image"])
            )


@bot.command()
@commands.has_permissions(administrator=True)
async def setup_panel(ctx):

    await ctx.send(
        "報告パネル",
        view=ReportView()
    )


@bot.event
async def on_ready():

    bot.add_view(ReportView())

    print(f"Logged in as {bot.user}")


bot.run(TOKEN)