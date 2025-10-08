import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.env import env
from core.messages import gemini_response_message

logger = logging.getLogger(__name__)


class GeminiCog(commands.Cog):
    """단어 검색을 위한 Gemini AI 통합 Cog."""

    def __init__(self, bot: commands.Bot) -> None:
        """GeminiCog 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        self.bot = bot

    @app_commands.command(
        name="단어검색", description="LLM으로 단어의 의미를 검색합니다."
    )
    @app_commands.describe(input_word="검색할 단어")
    async def gemini_response_command(
        self, interaction: discord.Interaction, input_word: str
    ) -> None:
        try:
            # 디스코드에게 생각중이라는 상태 전달
            await interaction.response.defer(thinking=True)

            gemini_client = self.bot.get_gemini_client(
                env.GEMINI_WORD_SEARCH_INSTRUCTION
            )
            status_code, response = await gemini_client.create_gemini_message(
                input_word
            )
            if status_code:
                text = gemini_response_message(interaction.user.mention, response)
            else:
                text = response

            # 생각중이라는 상태를 끝내고, 최종 결과 반환
            await interaction.followup.send(text)
        except discord.errors.HTTPException as e:
            logger.error(f"Discord HTTP 오류: {e}")
            try:
                await interaction.followup.send("응답을 보내는 중 오류가 발생했다 삐!")
            except Exception:
                pass
        except Exception as e:
            logger.error(f"단어 검색 중 예상치 못한 오류: {e}", exc_info=True)
            try:
                await interaction.followup.send("예상치 못한 오류가 발생했다 삐!")
            except Exception:
                pass


async def setup(bot):
    await bot.add_cog(GeminiCog(bot))
