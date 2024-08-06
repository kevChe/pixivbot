import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from db import DB

load_dotenv()

class Bot(commands.Bot):


    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = discord.Intents.all(),
            application_id = os.getenv("DISCORD_APPLICATION_ID")
        )
        self.db = DB()

    async def load(self):
        for f in os.listdir("./cogs"):
            if f.endswith('.py'):
                cog_name = f'cogs.{f[:-3]}'
                print(cog_name)
                await self.load_extension(cog_name)

    async def setup_hook(self):
        await self.load()
        await bot.tree.sync(guild = discord.Object(id = 1021667971682287627))

    async def on_ready(self):
        print(f'Park Online')

    async def close(self):
        self.close_db()
        print("Database connection closed")
        await super().close()

    def get_db(self):
        return self.db
    
    def close_db(self):
        self.db.close()

bot = Bot()
bot.run(os.getenv("DISCORD_TOKEN"))