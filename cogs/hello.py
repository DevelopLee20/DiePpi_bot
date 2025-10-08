import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.messages import hello_message

logger = logging.getLogger(__name__)


class HelloCog(commands.Cog):
    """간단한 인사 명령어를 제공하는 Cog."""

    def __init__(self, bot: commands.Bot) -> None:
        """HelloCog 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        self.bot = bot

    @app_commands.command(name="안녕", description="죽어삐가 인사를 건넵니다.")
    async def hello_text_command(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(
                hello_message(interaction.user.mention)
            )
        except discord.errors.HTTPException as e:
            logger.error(f"인사 메시지 전송 실패: {e}")
        except Exception as e:
            logger.error(f"인사 명령어 중 예상치 못한 오류: {e}", exc_info=True)


async def setup(bot):
    await bot.add_cog(HelloCog(bot))
