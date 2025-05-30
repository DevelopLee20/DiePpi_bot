import logging

import discord
from discord.ext import commands

from core.env import env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} 준비완료다 삐!")


# 채널 이름 설정
if env.MODE == "PROD":
    MODE_output = "☑️ PROD mode."
    STUDY_CHANNEL = "공부방"
    ALERT_CHANNEL = "스터디-알림"
else:
    MODE_output = "☑️ DEV mode."
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

    for idx, ext in enumerate(extensions_name):
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ {idx + 1}/{len(extensions_name)} {ext} loaded.")
        except Exception as e:
            logger.error(f"❌ Failed to load {ext}: {e}")

    logger.info(MODE_output)


if __name__ == "__main__":
    bot.run(env.TOKEN)
