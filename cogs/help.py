from discord.ext import commands
import discord
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Zeigt eine Liste an möglichen Commands an")
    async def help(self, interaction: discord.Interaction):
        embed=discord.Embed(title='Help', description='Bei Fragen blubb anschreiben. Hier kommt später eine Liste an möglichen Commands hin.', color=0xc69c6d)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        #falls ich noch was senden möchte response.followup

async def setup(bot):
    await bot.add_cog(Help(bot))
