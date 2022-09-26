import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
from DiscordChatExporterPy.chat_exporter import chat_exporter
import sql_methods

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()



"""
This is the archive cog. It is responsible for archiving channels.
"""
class Archive(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name= 'archive', description = 'archives a channel')
    async def archive(self, interaction: discord.Interaction, channel:str) -> None:
        guild = interaction.guild
        channel: discord.TextChannel = discord.utils.get(guild.channels, name = channel)
        if (channel == None):
            await interaction.response.send_message("Channel does not exist", ephemeral=True) #when someone tries to archive a channel that doesn't exist
            return
        if (channel.id == interaction.channel.id):
            await interaction.response.send_message("You might want to archive this from another channel!", ephemeral=True) #You need to archive channels from another channel
            return
        
        if (channel.permissions_for(interaction.user).manage_channels == True or sql_methods.getChannel(channel.name)[3] == interaction.user.id):
            file = await chat_exporter.quick_export(channel)
            await interaction.response.send_message(f'Channel {channel} archived', file=file, ephemeral=True) #when a channel is successfully archived
            await channel.delete()
            owner = sql_methods.getOwner(channel.id)
            sql_methods.removeChannel(channel.id)
            sql_methods.updateUser(owner, -1)
        else:
            await interaction.response.send_message("You do not have permission to archive this channel", ephemeral=True) #when the user did not create the channel or does not have manage channel permissions
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(Archive(bot))