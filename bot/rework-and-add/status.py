import datetime

from discord.ext import commands, tasks

from util_functions import *


class Status(commands.Cog):
    """This cog keeps the bot status in sync"""

    def __init__(self, bot):
        self.bot = bot

        self.status_task.start()
        self.uptime_logger.start()

        self.upt = 0

    def cog_unload(self):
        self.status_task.cancel()
        self.uptime_logger.cancel()

    async def set_default_status(self):
        ac_type = None

        if os.getenv("DEFAULT_STATUS_TYPE") == "watching":
            ac_type = discord.ActivityType.watching
        elif os.getenv("DEFAULT_STATUS_TYPE") == "listening":
            ac_type = discord.ActivityType.listening
        elif os.getenv("DEFAULT_STATUS_TYPE") == "streaming":
            ac_type = discord.ActivityType.streaming

        total = 0
        if "{number_users}" in os.getenv("DEFAULT_STATUS_TEXT"):
            guilds = self.bot.guilds
            for guild in guilds:
                total += guild.member_count

        if ac_type is None:
            ac_type = discord.ActivityType.playing

        await self.bot.change_presence(
            activity=discord.Activity(
                type=ac_type,
                name=os.getenv("DEFAULT_STATUS_TEXT")
                .replace("{guild_count}", str(len(list(self.bot.guilds))))
                .replace("{number_users}", str(total)),
            )
        )

    @commands.Cog.listener()
    async def on_ready(self):
        syslog.log("Bot Status", "Setting default status as per config")
        await self.set_default_status()

    @tasks.loop(seconds=60.0)
    async def status_task(self):
        await self.set_default_status()

    @status_task.before_loop
    async def before_status_task(self):
        syslog.log(
            "Bot Status", "Waiting for bot to be ready before starting updater task"
        )
        await self.bot.wait_until_ready()
        syslog.log("Bot Status", "Bot is ready. Enabling update task")

    @tasks.loop(seconds=1.0)
    async def uptime_logger(self):
        self.upt += 1

    @uptime_logger.before_loop
    async def before_logger_task(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=["uptime"])
    async def get_uptime(self, ctx):
        await ctx.send(
            embed=inf_msg(
                "Bot Stats",
                "Uptime: `" + str(datetime.timedelta(seconds=self.upt)) + "`",
            )
        )


async def setup(bot):
    await bot.add_cog(Status(bot))
