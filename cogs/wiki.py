from discord.ext import commands
import discord
from discord import app_commands
import requests
import asyncio
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
import urllib.parse

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="wiki", description="Search the SoT Wiki")   
    @app_commands.choices(amount_of_results=[
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3 (Default)", value=3),
        app_commands.Choice(name="4", value=4),
        app_commands.Choice(name="5", value=5),
        app_commands.Choice(name="6", value=6),
        app_commands.Choice(name="7", value=7),
        app_commands.Choice(name="8", value=8),
        app_commands.Choice(name="9", value=9),])
    async def wiki(self, interaction: discord.Interaction, search: str, amount_of_results: app_commands.Choice[int] = None):
        #CONFIG
        botColor = 0x000000
        theLine = "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        theLineExtension = "⎯⎯⎯⎯⎯⎯⎯"
        loadingIcon = "<a:loading:1161668117861249134>"
        if amount_of_results == None:
            amount_of_results = 3
        else:
            amount_of_results = amount_of_results.value
        base_url = 'https://seaofthieves.wiki.gg/api.php'



        #SEARCH (result_list, urls)
        try:
            searchParams = {
                "action": "opensearch",
                "format": "json",
                "search": search,
                "limit": amount_of_results
            }
            searchResponse = requests.get(base_url, params=searchParams)
            if searchResponse.status_code == 200:
                sData = searchResponse.json()
                result_list = sData[1]
                urls = sData[3]
            if not result_list:
                failEmbed=discord.Embed(title="Inputbeard", 
                                        description=f"There are **no** search results for **{search}** in the Sea of Thieves Wiki.", 
                                        color=botColor)
                failEmbed.add_field(name="Link to all articles", value=f"https://seaofthieves.wiki.gg/index.php?title=Special:AllPages", inline=False)
                failEmbed.set_thumbnail(url=self.bot.user.avatar.url)
                await interaction.response.send_message(embed=failEmbed, ephemeral=True)
        except Exception as s:
            print(s)
        

        #INBETWEEN
        #search result formatting
        emoji_mapping = {
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣',
        7: '7️⃣',
        8: '8️⃣',
        9: '9️⃣',
        }
        #check for single result
        if len(result_list) == 1:
            page_title = result_list[0]
            page_url = urls[0]
            run = True
            loadingEmbed=discord.Embed(title="",
                                description=f"There was only one result. Loading page {loadingIcon}",
                                color=botColor)
            await interaction.response.send_message(embed=loadingEmbed)
            print(page_url)
        else:
            #make results printable
            search_results = "\n".join([f"{emoji_mapping.get(i + 1, '❌')} {name}\n" for i, name in enumerate(result_list)])
            #search results embed send
            resultsEmbed=discord.Embed(title=f'Search Results for "{search}"', 
                                description=f"{search_results}", 
                                color=botColor)
            await interaction.response.send_message(embed=resultsEmbed)
            #add reactions to search result embed
            msg = await interaction.original_response()
            for i in range(1, len(result_list) + 1):
                number_emoji = f"{i}\uFE0F\u20E3"
                await msg.add_reaction(number_emoji)
            await msg.add_reaction("❌")

            #check reactions
            def check(reaction, user):
                return user == interaction.user and reaction.message.id == msg.id     
            try:
                reaction = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                emoji = reaction[0].emoji
                user_reaction = None
                for key, value in emoji_mapping.items():
                    if emoji == value:
                        user_reaction = key
                        break
                run = True
                if emoji == "❌":
                    run = False
            except asyncio.TimeoutError:
                await interaction.followup.send(content=f"{interaction.user.mention} did not react in time.")
            #except Exception as e1:
                #print(e1)
            await msg.clear_reactions()
            
            if run:
                #loading page information
                loadingEmbed=discord.Embed(title="",
                                    description=f"Loading page {loadingIcon}",
                                    color=botColor)
                await interaction.edit_original_response(embed=loadingEmbed)
            else:
                await interaction.delete_original_response()
            page_title = result_list[user_reaction - 1]
            page_url = urls[user_reaction - 1]


        #RESULTS
        #get pageid
        try:
            idParams = {
                "action": "query",
                "format": "json",
                "indexpageids": 1,
                "titles": page_title
            }
            idResponse = requests.get(base_url, params=idParams)
            if idResponse.status_code == 200:
                iData = idResponse.json()
                page_id = iData['query']['pageids'][0]
        except Exception as idex:
            execptionEmbed=discord.Embed(title=theLine,
                                description=f"# Idbeard \nError Code: \n{idex} \n\n{theLine}{theLineExtension}", 
                                color=botColor)
            await interaction.response.edit_original_response(embed=execptionEmbed)
        
        try:
            parseParams = {
                'action': 'parse',
                'format': 'json',
                'page': page_title,
            }
            queryParams = {
                "action": "query",
                "format": "json",
                "prop": "revisions",
                "titles": page_title,
                "rvprop": "timestamp|user"
            }

            #API requests
            parseResponse = requests.get(base_url, params=parseParams)
            queryResponse = requests.get(base_url, params=queryParams)

            # Check if the request was successful
            if parseResponse.status_code == 200 and queryResponse.status_code == 200:
                #get first paragraph
                pData = parseResponse.json()
                qData = queryResponse.json()
                page_content = pData['parse']['text']['*']
                soup = BeautifulSoup(page_content, 'html.parser')
                first_paragraph = soup.find('p').get_text()
                #get title
                title = pData.get('parse', {}).get('title', '')
                #get image
                images = pData.get('parse', {}).get('images', [])
                print(images)
                #match = re.search(rf'(href|src)="/images/.*?/{images[0]}"', page_content)
                #escaped_image = re.escape(images[0])
                print(images[0])
                imagename = urllib.parse.quote(images[0])
                print(imagename)
                pattern = rf'(href|src)="/images/[^"]*?{imagename}"'
                match = re.search(pattern, page_content)
                print(match)
                print(match.group())
                #src="/images/thumb/e/ef/Sea_of_Thieves_Insider_logo.png/361px-Sea_of_Thieves_Insider_logo.png"
                input_string = match.group()
                pattern2 = r'(src|href)="?'
                imagend = re.sub(pattern2, '', input_string)
                print(imagend)
                imagend = imagend.replace('"', '')
                print(imagend)
                
                try:
                    #/images/thumb/e/ef/Sea_of_Thieves_Insider_logo.png
                    if match:
                        image_url = f"https://seaofthieves.wiki.gg{imagend}"
                    else:
                        image_url = "https://rarethief.com/wp-content/uploads/2022/11/sea-of-thieves-season-eight-sinking-ship-sloop-galleon.png"
                except Exception as immissing:
                    print(f"image missing: {immissing}")
                    image_url = "https://rarethief.com/wp-content/uploads/2022/11/sea-of-thieves-season-eight-sinking-ship-sloop-galleon.png"
                #get date
                rawTimestamp = qData['query']['pages'][page_id]['revisions'][0]['timestamp']
                timestamp = datetime.fromisoformat(rawTimestamp)
                date = timestamp.strftime("%d.%m.%Y")
                time = timestamp.strftime("%H:%M")
                #get article author
                articleAuthor = qData['query']['pages'][page_id]['revisions'][0]['user']

                #create embed
                contentEmbed=discord.Embed(title=title, 
                                url=page_url,
                                description=first_paragraph, 
                                color=botColor)
                contentEmbed.set_footer(icon_url="https://seaofthieves.wiki.gg/images/6/6c/Journal_icon.png", text=f"Last edited {date} at {time} by {articleAuthor}")
                contentEmbed.set_image(url=image_url)
                await interaction.edit_original_response(embed=contentEmbed)

            #Request Error
            else:
                errorEmbed=discord.Embed(title=theLine,
                                description=f"# Requestbeard \nRequest failed with status code: \n{parseResponse.status_code} \n\n{theLine}{theLineExtension}", 
                                color=botColor)
                await interaction.edit_original_response(embed=errorEmbed)
        #Exeption Error
        except Exception as e:
            execptionEmbed=discord.Embed(title=theLine,
                                description=f"# Exeptionbeard \nError Code: \n{e} \n\n{theLine}{theLineExtension}", 
                                color=botColor)
            await interaction.edit_original_response(embed=execptionEmbed)

async def setup(bot):
    await bot.add_cog(Wiki(bot))
