import discord
from discord.ext import commands
from discord import app_commands


class Archive(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name= 'archive', description = 'archives a channel')
    async def archive(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("test")


async def setup(bot: commands.Bot):
    await bot.add_cog(Archive(bot))