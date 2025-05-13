import discord
from discord.ext import commands

from core.env import env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 준비완료다 삐!")

# 명령어 추가
@bot.event
async def setup_hook():
    extensions_name = [
        "cogs.hello",
        "cogs.time_tracking",
    ]

    for ext in extensions_name:
        try:
            await bot.load_extension(ext)
            print(f"✅ {ext} loaded.")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

if __name__ == "__main__":
    bot.run(env.TOKEN)
