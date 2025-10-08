import logging

import discord
from discord.ext import commands

from core.config import BotConfig
from core.env import env
from db.client import close_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiePpiBot(commands.Bot):
    """DiePpi Discord Bot 클래스."""

    def __init__(self, *args, config: BotConfig, **kwargs):
        """DiePpiBot 초기화.

        Args:
            config: 봇 설정
        """
        super().__init__(*args, **kwargs)
        self.config = config


intents = discord.Intents.default()
intents.message_content = True

# 봇 설정
config = BotConfig.from_env()
bot = DiePpiBot(command_prefix=env.COMMAND_PREFIX, intents=intents, config=config)


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
        except commands.ExtensionNotFound as e:
            logger.error(f"❌ Extension {ext} not found: {e}")
        except commands.ExtensionFailed as e:
            logger.error(f"❌ Extension {ext} setup failed: {e}")
        except ImportError as e:
            logger.error(f"❌ Failed to import {ext}: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error loading {ext}: {e}", exc_info=True)

    await bot.tree.sync()
    logger.info(f"☑️ {config.mode} mode.")


if __name__ == "__main__":
    try:
        bot.run(env.TOKEN)
    finally:
        close_db_connection()
