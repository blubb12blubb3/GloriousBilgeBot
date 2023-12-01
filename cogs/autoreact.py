from discord.ext import commands
import discord
from discord import app_commands


class Autoreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() # Das gleiche wie in bot.event
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        #                   aktuelle-bewerbungen bewerbung-abstimmung
        reactionChannels = [1138220198030213220, 1140001438509039677]

        if message.channel.id in reactionChannels:
            await message.add_reaction(":ja:1147814140417691718")
            #await message.add_reaction(":unsicher:1147814173045162064")
            await message.add_reaction(":nein:1147814157417197578")

async def setup(bot):
    await bot.add_cog(Autoreact(bot))
