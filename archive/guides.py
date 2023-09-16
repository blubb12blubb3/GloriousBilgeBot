from discord.ext import commands
import discord
from discord import app_commands


class Guides(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="guides", description="guides und so")
    async def guides(self, interaction: discord.Interaction, subcommand1: str, arg1: str, arg2: str):
    
    

        await interaction.response.send_message("guides World")
        #falls ich noch was senden möchte response.followup

async def setup(bot):
    await bot.add_cog(Guides(bot))



from discord.ext import commands

class MultiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="multi", description="A command with multiple options")
    async def multi(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `help multi` for a list of available subcommands.")

    @multi.command(name="option1", description="First option")
    async def option1(self, ctx):
        await ctx.send("You selected option 1.")

    @multi.command(name="option2", description="Second option")
    async def option2(self, ctx):
        await ctx.send("You selected option 2.")

    @multi.command(name="option3", description="Third option")
    async def option3(self, ctx):
        await ctx.send("You selected option 3.")

async def setup(bot):
    bot.add_cog(MultiCommand(bot))

