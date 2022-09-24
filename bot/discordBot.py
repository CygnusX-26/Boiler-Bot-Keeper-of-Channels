import discord
import os
import sqlite3
from discord.ext import commands

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

db_path2 = 'users.db'
conn2 = sqlite3.connect(db_path2)
c2 = conn2.cursor()

class BoilerBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("DISCORD_BOT_PREFIX")),
            description='BoilerBot',
            intents=discord.Intents.all(),
            application_id = int(os.getenv("APPLICATION_ID")))
        
    async def load_extensions(self) -> None: 
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def setup_hook(self) -> None:
        self.remove_command('help')
        await self.load_extensions()
        await bot.tree.sync()

# creates a new user table if one doesn't currently exist
#very temp code xdxdxdxd
try:
    c.execute("""CREATE TABLE channels (
            name text,
            id integer,
            usercount integer,
            owner integer
            )""")

except sqlite3.OperationalError:
    pass

try: 
    c2.execute("""CREATE TABLE users (
            id integer,
            name text,
            channel integer
            )""")
except sqlite3.OperationalError:
    pass

bot = BoilerBot()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))