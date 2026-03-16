import discord
from discord.ext import commands
import os
import time
from discord import app_commands

# 修正済み
TOKEN = os.getenv("TRTM_DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("TRTM_DISCORD_TOKEN が設定されていません")

# サーバーID
GUILD_ID = 359006972290400257
guild = discord.Object(id=GUILD_ID)

# 修正予定！
TARGET_CHANNEL_ID = 1219311541300625529

# 修正済み
GITHUB_PAGES_BASE = "https://takashitara.github.io/trtm-bot/images"

# 修正予定
BUTTONS = [
    {"label": "撮影開始", "image": "rec.png"},
    {"label": "めい寝た", "image": "sleep.png"},
    {"label": "洗濯完了", "image": "wash.png"},
    {"label": "拡張可能１", "image": "ready.png"},
    {"label": "拡張可能２", "image": "back.png"},
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


class ReportButton(discord.ui.Button):

    def __init__(self, label, image):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary,
            custom_id=f"trtm_{label}"
        )
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

        user = interaction.user.mention

        await channel.send(
            content=f"{user} が **{self.label}** を押しました",
            embed=embed
        )

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


@bot.tree.command(name="setup_panel", description="報告パネルを表示")
async def setup_panel(interaction: discord.Interaction):

    await interaction.response.send_message(
        "報告パネル",
        view=ReportView()
    )


@bot.event
async def on_ready():

    bot.add_view(ReportView())
    await bot.tree.sync()

    print(f"Logged in as {bot.user}")


bot.run(TOKEN)