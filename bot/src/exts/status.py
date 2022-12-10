import datetime, yaml, asyncio

from disnake.ext import commands, tasks

from .util_functions import *


class Status(commands.Cog):
    """This cog keeps the bot status in sync"""

    def __init__(self, bot):
        self.bot = bot

        self.status_task.start()
        self.uptime_logger.start()

        self.upt = 0

        with open("conf.yml", "r") as stream:
            try:
                self.fconfig = yaml.safe_load(stream)
            except yaml.YAMLError as err:
                print(err)

    def cog_unload(self):
        self.status_task.cancel()
        self.uptime_logger.cancel()

    async def set_default_status(self):
        ac_type = None

        await asyncio.sleep(10)

        if self.fconfig["DEFAULT_STATUS_TYPE"] == "watching":
            ac_type = disnake.ActivityType.watching
        elif self.fconfig["DEFAULT_STATUS_TYPE"] == "listening":
            ac_type = disnake.ActivityType.listening
        elif self.fconfig["DEFAULT_STATUS_TYPE"] == "streaming":
            ac_type = disnake.ActivityType.streaming

        total = 0
        if "{number_users}" in self.fconfig["DEFAULT_STATUS_TEXT"]:
            guilds = self.bot.guilds
            for guild in guilds:
                total += guild.member_count

        if ac_type is None:
            ac_type = disnake.ActivityType.playing

        await self.bot.change_presence(
            activity=disnake.Activity(
                type=ac_type,
                name=self.fconfig["DEFAULT_STATUS_TEXT"]
                .replace("{guild_count}", str(len(list(self.bot.guilds))))
                .replace("{number_users}", str(total)),
            )
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setting default status as per config")
        await self.set_default_status()

    @tasks.loop(seconds=60.0)
    async def status_task(self):
        await self.set_default_status()

    @status_task.before_loop
    async def before_status_task(self):
        print("Waiting for bot to be ready before starting updater task")
        await self.bot.wait_until_ready()
        print("Bot is ready. Enabling update task")

    @tasks.loop(seconds=1.0)
    async def uptime_logger(self):
        self.upt += 1

    @uptime_logger.before_loop
    async def before_logger_task(self):
        await self.bot.wait_until_ready()

    @commands.slash_command(name="getuptime")
    async def get_uptime(self, inter):
        """How long has the bot been running?"""
        await inter.send(
            embed=inf_msg(
                "Bot Stats",
                "Uptime: `" + str(datetime.timedelta(seconds=self.upt)) + "`",
            )
        )


def setup(bot):
    print("Loading status ext")
    bot.add_cog(Status(bot))
