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
    try:
        await bot.load_extension("cogs.hello")
        print("✅ cogs.hello loaded")
    except Exception as e:
        print(f"❌ Failed to load cogs.hello: {e}")

    try:
        await bot.load_extension("cogs.time_tracking")
        print("✅ cogs.time_tracking loaded")
    except Exception as e:
        print(f"❌ Failed to load cogs.time_tracking: {e}")

if __name__ == "__main__":
    bot.run(env.TOKEN)
