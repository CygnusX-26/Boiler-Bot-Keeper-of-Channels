from webbrowser import get
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import sqlite3
import sql_methods

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

class Channel(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #hides a channel
    @app_commands.command(name= 'hidechannels', description = 'hides a channel')
    async def hideChannels(self, interaction: discord.Interaction) -> None:
        if (sql_methods.getAllChannels() == []):
            await interaction.response.send_message("No channels avaliable!", ephemeral=True)
            return
        await interaction.response.send_message('Choose a channel!', view=SelectView(interaction.guild, interaction), ephemeral=True)



class Select(ui.Select):
    def __init__(self, guild: discord.Guild, interaction: discord.Interaction):
        allChannels = sql_methods.getAllChannels()
        options=[]
        for i in allChannels:
            channel = discord.utils.get(guild.channels, id=sql_methods.getChannel(i[0])[1])
            if (channel.permissions_for(interaction.user).view_channel == True):
                options.append(discord.SelectOption(label=f"{i[0]}", description=f"{i[2]} member(s)"))
        super().__init__(placeholder="Select a channel", min_values=1, max_values=len(options), options=options)
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        message = ""
        for i in self.values:
            if sql_methods.getChannel(i) is None:
                message += f'Channel {i} does not exist\n'
                continue
            channel = discord.utils.get(guild.channels, id=sql_methods.getChannel(i)[1])
            if (channel.permissions_for(interaction.user).view_channel == False):
                message += f"You don't have access to {channel.name}\n"
                continue
            await channel.set_permissions(interaction.user, view_channel=False)
            await channel.edit(category=discord.utils.get(guild.categories, name="Channels"))
            message += f'Channel {channel.name} updated\n'
            sql_methods.updateChannel(i, channel.id, -1)
        await interaction.response.send_message(message, ephemeral=True)



class SelectView(ui.View):
    def __init__(self, guild:discord.Guild, interaction:discord.Interaction, *, timeout=100):
        super().__init__(timeout=timeout)
        self.add_item(Select(guild, interaction))



async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))