import discord
from discord.ext import commands
import asyncio
import os
from tk import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=None, intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} eingeloggt")
    game = discord.Game("Sea of Thieves")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f"{bot.user} is ready but not synced yet.")
    slashsync = await bot.tree.sync()
    print(f"{bot.user} {len(slashsync)} commands synced.")


async def load_extensions():
    async def load_cogs(dir):
        for filename in os.listdir(dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    await bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Cogs loaded from {dir}")
    dir1 = "./Hugin/cogs"
    dir2 = "./cogs"
    if os.path.exists(dir1):
        await load_cogs(dir1)
    elif os.path.exists(dir2):
        await load_cogs(dir2)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token=TOKEN)

asyncio.run(main())
