from discord.ext import commands
import discord
from discord import app_commands


class Onlyfans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="onlyfans", description="cooles gif")
    async def onlyfans(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://giphy.com/gifs/jiggle-sea-of-thieves-jollyjiggle-a12b7RO0kGMldmK6dy")
        #falls ich noch was senden möchte response.followup

async def setup(bot):
    await bot.add_cog(Onlyfans(bot))
