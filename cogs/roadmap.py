from discord.ext import commands
import discord
from discord import app_commands


class Roadmap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roadmap", description="Was für die Zukunft geplant ist")
    async def roadmap(self, interaction: discord.Interaction):
        embed=discord.Embed(title="Roadmap für den Glorious Bilge Bot", description="Hier steht was für die Zukunft von dem Bot geplant ist. Bei Wünschen, schreibt gerne eine Nachricht an blubb12blubb3.", color=0xc59d6d)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        #Ziel 1
        embed.add_field(name="/help", value="- Ein Command, wo man für jeden Command eine Erklärung bekommen kann", inline=False)
        #Ziel 2
        embed.add_field(name="Überarbeitung von /wiki", value="- Code optimieren \n- Bugfix für kurze Wörter die in den Wiki-URLs klein geschrieben werden, z.B: Of - of \n- Error Messages nur dem User, der den Command benutzt hat, anzeigen", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roadmap(bot))