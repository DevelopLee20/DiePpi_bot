from discord.ext import commands

from core.gemini_client import GeminiClient
from core.messages import gemini_response_message


class GeminiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini = GeminiClient("50자 이내;간단한 설명;문장끝은 항상 삐!")

    @commands.command(name="단어검색")
    async def gemini_response_command(self, ctx, input_word: str):
        status_code, response = await self.gemini.create_gemini_message(input_word, ctx)
        if status_code:
            text = gemini_response_message(ctx.author.mention, response)
        else:
            text = response

        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(GeminiCog(bot))
