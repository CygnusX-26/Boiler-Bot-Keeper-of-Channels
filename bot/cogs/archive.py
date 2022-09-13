import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
from DiscordChatExporterPy.chat_exporter import chat_exporter

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

def removeChannel(id:int):
    with conn:
        c.execute(f"DELETE from channels WHERE id = ?", (id,))



"""
This is the archive cog. It is responsible for archiving channels.
"""
class Archive(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name= 'archive', description = 'archives a channel')
    async def archive(self, interaction: discord.Interaction, channel:discord.TextChannel) -> None:
        if (channel.id == interaction.channel.id):
            await interaction.response.send_message("You might want to archive this from another channel!", ephemeral=True)
            return
        if (channel.permissions_for(interaction.user).manage_channels == True ):
            file = await chat_exporter.quick_export(channel)
            await interaction.response.send_message(f'Channel {channel} archived', file=file, ephemeral=True)
            await channel.delete()
            removeChannel(channel.id)
        else:
            interaction.response.send_message("You do not have permission to archive this channel", ephemeral=True)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(Archive(bot))