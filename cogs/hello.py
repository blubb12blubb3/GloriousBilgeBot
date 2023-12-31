from discord.ext import commands
import discord
from discord import app_commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Guten Tag")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World")
        #falls ich noch was senden möchte response.followup

async def setup(bot):
    await bot.add_cog(Hello(bot))
