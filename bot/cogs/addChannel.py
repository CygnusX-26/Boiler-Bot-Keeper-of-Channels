import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import sqlite3

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

def insertChannel(name:str, id:int, current:int) -> None:
    with conn:
        c.execute(f"INSERT INTO channels VALUES (?, ?, ?)", (name, id, current))

def getUserCount(name, id):
    c.execute(f"SELECT * FROM channels WHERE name = ? AND id = ?", (name, id))
    return c.fetchone()[2]


class addChannel(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    
    @app_commands.command(name= 'createchannel', description = 'Creates a new channel')
    async def createChannel(self, interaction: discord.Interaction, name:str) -> None:
        guild = interaction.guild
        channel = await guild.create_text_channel(f'{name}')
        insertChannel(name, channel.id, 0)
        await channel.set_permissions(guild.default_role, view_channel=False)
        await interaction.response.send_message(f'Channel {channel} created', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(addChannel(bot))