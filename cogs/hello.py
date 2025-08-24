import discord
from discord import app_commands
from discord.ext import commands

from core.messages import hello_message


class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="안녕", description="죽어삐가 인사를 건넵니다.")
    async def hello_text_command(self, interaction: discord.Interaction):
        await interaction.response.send_message(hello_message(interaction.user.mention))


async def setup(bot):
    await bot.add_cog(HelloCog(bot))
