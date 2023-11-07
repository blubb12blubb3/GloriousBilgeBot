from discord.ext import commands
import discord
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Zeigt eine Liste an möglichen Commands an")
    async def help(self, interaction: discord.Interaction):

        with open('./Glorious_Bilge_Bot/text/help.txt', 'r') as file:
            file_contents = file.read()      

        embed=discord.Embed(title="Roadmap für den Glorious Bilge Bot", description=file_contents, color=0xc59d6d)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
