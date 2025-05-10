import discord
from discord.ext import commands

from core.env import env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 준비완료!")

# 명령어 추가
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.hello")

if __name__ == "__main__":
    bot.run(env.TOKEN)
