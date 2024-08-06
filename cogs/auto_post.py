from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord import app_commands, File
from db import DB
# from bot import Bot
from pixiv_scrape import Pixiv_scrape
import discord
import os
load_dotenv()

class auto_post(commands.Cog):

    @app_commands.command(name="hi", description="hihi")
    async def test(self, interaction: discord.Interaction):
        temp_message = await self.channel.send(file=File("a.jpg"))
        await interaction.response.send_message(f" {interaction.user.name}，hihi")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        #Initialize database
        self.db = DB()
        self.db = self.bot.get_db()

        # # 2KA SERVER TEST SETTING
        # self.guild = self.bot.get_guild(1021667971682287627)

        # # ACTUAL CHANNEL
        # self.channel = self.guild.get_channel(1022456930146451456)
        # self.r18channel = self.guild.get_channel(1028649755410173972)

        # # PIC BUFFER
        # self.channel = self.bot.get_channel(1026387611230670848)
        # self.r18channel = self.bot.get_channel(1026387611230670848)


        self.loop.start()
    

    @tasks.loop(minutes=10)
    async def loop(self):
        try:
            for guild_info in self.db.find({}, "guilds"):
                guild = self.bot.get_guild(guild_info['_id'])
                print(guild_info['tags'])
                field_names = list(guild_info)
                if 'nsfw' in field_names:
                    for channel_id in guild_info['nsfw']:
                        channel = await guild.fetch_channel(channel_id)
                        await self.sendPic(channel, True)
                if 'sfw' in field_names:
                    for channel_id in guild_info['sfw']:
                        channel = guild.get_channel(channel_id)
                        await self.sendPic(channel, False)
            # await self.sendPic(self.channel, False)
            # await self.sendPic(self.r18channel, True)
        except Exception as e:
            print(e)

    async def sendPic(self, channel, r18):
        rand_pic_details = self.getRandomPic(r18)
        url= rand_pic_details[0]['url']
        local_filename = url.split('/')[-1]
        pixiv_url=f"<https://www.pixiv.net/artworks/{rand_pic_details[0]['_id']}>"
        Pixiv_scrape.download_pic(url, local_filename)
        await channel.send(pixiv_url, file=File(local_filename))
        os.remove(local_filename)

    def getRandomPic(self, r18) -> File:
        filter = [
            {"$match": {"r18": r18}},
            {'$sample': {"size": 1}}
        ]
        random = self.db.pickRandom(filter, "links")
        return random

    @app_commands.command(name="set_channel")
    @app_commands.describe(channel_id = "輸入你想要自動放圖的頻道id", r18 = "色圖請選擇True，否則請選擇False")
    # @app_commands.rename(channel_id = "Channel ID", r18 = "r18")
    async def addChannel(self, interaction: discord.Interaction, channel_id: str, tags: str, r18: bool, time: app_commands.Choice[int]):
        guild = interaction.guild_id
        channel_r18 = "nsfw" if r18 else "sfw"
        self.db.update({"_id": guild}, {"$push": {"tags": tags, channel_r18: channel_id}}, "guilds")
        await interaction.response.send_message(guild)

    @app_commands.command(name="set_post_time")
    @app_commands.choices(time=[
        app_commands.Choice(name="半小時", value=30),
        app_commands.Choice(name="一小時", value=60)
        ])
    async def post_time(self, interaction: discord.Interaction, time: app_commands.Choice[int]):
        # print(time.value)
        self.db.update({"_id": interaction.guild_id}, {"$set": {"time": time.value}}, "guilds")
        await interaction.response.send_message(f"Post time interval setted to every {time.value} minutes")


async def setup(bot):
    await bot.add_cog(auto_post(bot), guild= discord.Object(id = 1021667971682287627))