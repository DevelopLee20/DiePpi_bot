from discord.ext import commands


class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="안녕")
    async def hello_text_command(self, ctx):
        await ctx.send(f"{ctx.author.mention} 안녕하세요! 삐!")


async def setup(bot):
    await bot.add_cog(HelloCog(bot))
