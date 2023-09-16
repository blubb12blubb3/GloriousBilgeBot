from discord.ext import commands
import discord
from discord import app_commands


class Guide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="guide", description="Verschieden Video und Bilder Guides")
    @app_commands.choices(type=[
        app_commands.Choice(name="Megalodons", value="meg")])
    async def guide(self, interaction: discord.Interaction, type: app_commands.Choice[str]):
        if type.value == "meg":
            await interaction.response.send_message("https://www.youtube.com/watch?v=ESWT4BaP050")
        

async def setup(bot):
    await bot.add_cog(Guide(bot))