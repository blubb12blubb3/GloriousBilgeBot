from discord.ext import commands
import discord
from discord import app_commands
import requests

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="wiki", description="Durchsucht das SoT Wiki")

    async def wiki(self, interaction: discord.Interaction, search: str, page_anchor: str = None):

    #search formatting
        unformatted_search = search
        search = search.title()
        search = search.replace(" ", "_")

        search_text = "There is currently no text in this page. You can search for this page title in other pages, or search the related logs, but you do not have permission to create this page."

        if page_anchor == None:
            url = f"https://seaofthieves.fandom.com/wiki/{search}"
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text
                if search_text in page_content:
                    await interaction.response.send_message(f"Geb bitte blubb Bescheid, wenn ich das hier ausgespuckt habe. Dann ist etwas mit mir falsch (Code: wiki01)") #ERROR CODE: wiki01
                else:
                    await interaction.response.send_message(f"https://seaofthieves.fandom.com/wiki/{search}")
            else:
                embed=discord.Embed(title="That Article Doesn't Exist.", 
                                    description=f"There is **no** wiki article on **{search}**. Make sure you have spelled everything correctly. You don't have to pay attention to upper and lower case but make sure to include all spaces.", 
                                    color=0xc69c6d)
                embed.add_field(name="search", value=f"{unformatted_search}", inline=True)
                embed.add_field(name="page_anchor", value="-", inline=True)
                embed.add_field(name="Link To Missing Article", value=f"https://seaofthieves.fandom.com/wiki/{search}", inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                await interaction.response.send_message(embed=embed)

        elif page_anchor != None:
        #page_anchor formatting
            unformatted_page_anchor = page_anchor
            page_anchor = page_anchor.title()
            page_anchor = page_anchor.replace(" ", "_")

            url = f"https://seaofthieves.fandom.com/wiki/{search}#{page_anchor}"

            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text
                if search_text in page_content:
                    await interaction.response.send_message(f"Geb bitte blubb Bescheid, wenn ich das hier ausgespuckt habe. Dann ist etwas mit mir falsch (Code: wiki02)") #ERROR CODE: wiki02
                else:
                    await interaction.response.send_message(f"https://seaofthieves.fandom.com/wiki/{search}#{page_anchor}")
            else:
                embed=discord.Embed(title="That Article Doesn't Exist.", 
                                    description=f"There is **no** wiki article on **{search}**. Make sure you have spelled everything correctly. You don't have to pay attention to upper and lower case but make sure to include all spaces.", 
                                    color=0xc69c6d)
                embed.add_field(name="search", value=f"{unformatted_search}", inline=True)
                embed.add_field(name="page_anchor", value=f"{unformatted_page_anchor}", inline=True)
                embed.add_field(name="Link To Missing Article", value=f"https://seaofthieves.fandom.com/wiki/{search}#{page_anchor}", inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(Wiki(bot))