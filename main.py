import logging

import discord
from discord.ext import commands

from core.config import BotConfig
from core.env import env
from db.client import close_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# 봇 설정
config = BotConfig.from_env()
bot.config = config  # Cog에서 접근할 수 있도록 bot에 설정 저장


@bot.event
async def on_ready():
    logger.info(f"{bot.user} 준비완료다 삐!")


# 명령어 추가
@bot.event
async def setup_hook():
    extensions_name = [
        "cogs.hello",
        "cogs.time_tracking",
        "cogs.role_change",
        "cogs.gemini",
    ]

    for idx, ext in enumerate(extensions_name):
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ {idx + 1}/{len(extensions_name)} {ext} loaded.")
        except Exception as e:
            logger.error(f"❌ Failed to load {ext}: {e}")

    await bot.tree.sync()
    logger.info(f"☑️ {config.mode} mode.")


@bot.event
async def close():
    """봇 종료 시 DB 연결 정리"""
    logger.info("봇 종료 중... DB 연결 정리")
    close_db_connection()


if __name__ == "__main__":
    try:
        bot.run(env.TOKEN)
    finally:
        close_db_connection()
