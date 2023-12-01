from discord.ext import commands
import discord
from discord import app_commands


class Abstimmung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="abstimmung", description="Füge Reaktionen für Abstimmungen zu einer bestimmten Nachricht hinzu")
    async def abstimmung(self, interaction: discord.Interaction, nachricht: str):
        msg = nachricht

        if "discord" in msg:
            message_link = msg
            segments = msg.split("/")
            msg_id = segments[-1]
        else:
            msg_id = msg
            message_link = (f"https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{msg}")

        message = await self.bot.get_channel(interaction.channel_id).fetch_message(msg_id)
        try:
            if "Reaction emoji=<Emoji id=1147814140417691718 name='ja' animated=False managed=False> me=True" \
                and "Reaction emoji=<Emoji id=1147814157417197578 name='nein' animated=False managed=False> me=True" in str(message.reactions):
                    await message.remove_reaction(":ja:1147814140417691718",self.bot.user)
                    #await message.remove_reaction(":unsicher:1147814173045162064",self.bot.user)
                    await message.remove_reaction(":nein:1147814157417197578",self.bot.user)
                    await interaction.response.send_message(f"Reaktionen von {message_link} entfernt", ephemeral=True)
            else:
                await message.add_reaction(":ja:1147814140417691718")
                #await message.add_reaction(":unsicher:1147814173045162064")
                await message.add_reaction(":nein:1147814157417197578")
                await interaction.response.send_message(f"Reaktionen zu {message_link} hinzugefügt", ephemeral=True)
        except:
            await interaction.response.send_message(f"Nachricht nicht gefunden. Link: {message_link}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Abstimmung(bot))

#and "Reaction emoji=<Emoji id=1147814173045162064 name='unsicher' animated=False managed=False> me=True" \
#insert after line 24 if want to go back
