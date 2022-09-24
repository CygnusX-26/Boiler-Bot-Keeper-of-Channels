import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import sql_methods

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

"""
   Adds a channel to the database + creates the channel
"""
class addChannel(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    
    @app_commands.command(name= 'createchannel', description = 'Creates a new channel')
    async def createChannel(self, interaction: discord.Interaction, name:str) -> None:
        if (sql_methods.getUser(interaction.user.id) is None):
            sql_methods.insertUser(interaction.user.id, interaction.user.name)
        if (sql_methods.getChannel(name) == None):
            print(sql_methods.getUser(interaction.user.id)[2])
            if (sql_methods.getUser(interaction.user.id)[2] > 4):
                await interaction.response.send_message("No more than 5 channels!", ephemeral=True)
                return
            guild = interaction.guild
            if (discord.utils.get(guild.categories, name = 'Channels') != None):
                category = discord.utils.get(guild.categories, name = 'Channels')
            else:
                category = await guild.create_category('Channels')
            await category.set_permissions(guild.default_role, view_channel=False)
            channel = await guild.create_text_channel(f'{name}', category=category)
            sql_methods.insertChannel(name, channel.id, 0, interaction.user.id)
            sql_methods.updateUser(interaction.user.id, 1)
            await channel.set_permissions(guild.default_role, view_channel=False)
            await interaction.response.send_message(f'Channel {channel} created', ephemeral=True)
        else:
            await interaction.response.send_message(f'Channel {name} already exists', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(addChannel(bot))