import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
import sql_methods


class MyChannels(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
            

   #someone can make this embed better PLZ :sob:
    @app_commands.command(name= 'mychannels', description = 'Gets a list of your channels')
    async def myChannels(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title = "Your Channels", color = 0x36393F)
        for channel in sql_methods.getAllChannels():
            if (channel[3] == interaction.user.id):
                embed.add_field(name = channel[0], value = f"> Members: {channel[2]}", inline = False)
        if (embed.fields == []):
            embed.add_field(name = "You have no channels", value = "> Create one with /createchannel", inline = False)
        await interaction.response.send_message(embed = embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MyChannels(bot))