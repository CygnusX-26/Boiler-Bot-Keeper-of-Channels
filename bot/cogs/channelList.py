from lib2to3.pgen2.token import OP
from optparse import Option
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.ui.select import SelectOption

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

def getChannel(name:str):
    c.execute(
        f"SELECT * FROM channels WHERE name = ?", (name,))
    return c.fetchone()

def updateChannel(name:str, id:int, inc:int) -> None:
    c.execute(f"SELECT * FROM channels WHERE id = ?", (id,))
    temp = c.fetchone()[2]
    with conn:
        c.execute(f"""UPDATE channels SET usercount = {temp + inc}
                WHERE name = ? AND id = ?
                """, (name, id))

def getAllChannels() -> list:
    c.execute(
        f"SELECT * FROM channels")
    return c.fetchall()

class ChannelList(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name= 'channels', description = 'gets a list of avaliable channels')
    async def channelList(self, interaction: discord.Interaction) -> None:
        if (getAllChannels() == []):
            await interaction.response.send_message("No channels avaliable!", ephemeral=True)
            return
        await interaction.response.send_message('Choose a channel!', view=SelectView(), ephemeral=True)


class Select(ui.Select):
    def __init__(self):
        allChannels = getAllChannels()
        options=[]
        for i in allChannels:
            options.append(discord.SelectOption(label=f"{i[0]}", description=f"{i[2]} member(s)"))
        super().__init__(placeholder="Select a channel", min_values=1, max_values=len(allChannels), options=options)
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        message = ""
        for i in self.values:
            if getChannel(i) is None:
                message += f'Channel {i} does not exist\n'
                continue
            channel = discord.utils.get(guild.channels, id=getChannel(i)[1])
            if (channel.permissions_for(interaction.user).view_channel == True):
                message += f'You already have access to {channel.name}\n'
                continue
            await channel.set_permissions(interaction.user, view_channel=True)
            message += f'Channel {channel.name} updated\n'
            updateChannel(i, channel.id, 1)
        await interaction.response.send_message(message, ephemeral=True)

class SelectView(ui.View):
    def __init__(self, *, timeout=100):
        super().__init__(timeout=timeout)
        self.add_item(Select())

async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelList(bot))







#temp code for later idk don't worry about this xd-----------------------------------------------------------------------------------------------------------





# class ChannelListSelect(ui.Modal, title='List of channels'):
#     def __init__(self):
#         super().__init__()
#         self.listOfAllChannels = getAllChannels()
#         self.add_item(ui.TextInput(label="Which page of channels?", placeholder="0", max_length=100))
    
#     async def on_submit(self, interaction: discord.Interaction) -> None:
#         allChannels = getAllChannels()
#         embed = discord.Embed(title="List of channels", description="List of channels", color=discord.Color.dark_blue())
#         message = ""
#         for i in allChannels:
#             message += f'> {i[0]} ▹ `{str(i[2])}` member(s)\n'
#         embed.add_field(name="Channels", value=message, inline=False)
#         await interaction.response.send_message(embed=embed, ephemeral=True)