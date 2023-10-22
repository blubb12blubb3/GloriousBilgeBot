from discord.ext import commands
import discord
from discord import app_commands


class Roadmap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roadmap", description="Was für die Zukunft geplant ist")
    async def roadmap(self, interaction: discord.Interaction):

        with open('./Glorious_Bilge_Bot/roadmap.txt', 'r') as file:
            file_contents = file.read()      

        embed=discord.Embed(title="Roadmap für den Glorious Bilge Bot", description=file_contents, color=0xc59d6d)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roadmap(bot))
