from discord.ext import commands

from core.messages import hello_message


class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="안녕")
    async def hello_text_command(self, ctx):
        await ctx.send(hello_message(ctx.author.mention))


async def setup(bot):
    await bot.add_cog(HelloCog(bot))
