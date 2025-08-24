import discord
from discord import app_commands
from discord.ext import commands

from core.gemini_client import GeminiClient
from core.messages import gemini_response_message


class GeminiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini = GeminiClient("50자 이내;간단한 설명;문장끝은 항상 삐!")

    @app_commands.command(
        name="단어검색", description="LLM으로 단어의 의미를 검색합니다."
    )
    @app_commands.describe(input_word="검색할 단어")
    async def gemini_response_command(
        self, interaction: discord.Interaction, input_word: str
    ):
        status_code, response = await self.gemini.create_gemini_message(input_word)
        if status_code:
            text = gemini_response_message(interaction.user.mention, response)
        else:
            text = response

        await interaction.response.send_message(text)


async def setup(bot):
    await bot.add_cog(GeminiCog(bot))
