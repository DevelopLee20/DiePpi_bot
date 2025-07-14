from discord.ext import commands
from google import genai
from google.genai import types

from core.env import env
from core.messages import gemini_response_message


class GeminiClient:
    def __init__(self, instruction: str):
        self.client = None
        self.instruction = instruction

    async def initialize(self):
        client = genai.Client(api_key=env.GEMINI_API_KEY)

        gemini_chat = client.chats.create(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(system_instruction=self.instruction),
        )

        self.client = gemini_chat

    async def create_gemini_message(self, input_word: str, ctx) -> tuple[bool, str]:
        if self.client is None:
            await self.initialize()
        try:
            return True, self.client.send_message(input_word).text
        except Exception as e:
            return False, f"GEMINI 오류 발생: {e}"


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
