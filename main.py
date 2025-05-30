import discord
from discord.ext import commands

from core.env import env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} 준비완료다 삐!")


# 채널 이름 설정
if env.MODE == "PROD":
    print("☑️ PROD mode.")
    STUDY_CHANNEL = "공부방"
    ALERT_CHANNEL = "스터디-알림"
else:
    print("☑️ DEV mode.")
    STUDY_CHANNEL = "디스코드-봇-만드는-채널"
    ALERT_CHANNEL = "디스코드-봇-만드는-채널"


# 명령어 추가
@bot.event
async def setup_hook():
    extensions_name = [
        "cogs.hello",
        "cogs.time_tracking",
        "cogs.role_change",
    ]

    for ext in extensions_name:
        try:
            await bot.load_extension(ext)
            print(f"✅ {ext} loaded.")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")


if __name__ == "__main__":
    bot.run(env.TOKEN)
