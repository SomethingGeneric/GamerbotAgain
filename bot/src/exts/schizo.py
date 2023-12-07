import datetime, asyncio, toml, random, disnake

from disnake.ext import commands, tasks

from .util_functions import *


class Schizo(commands.Cog):
    """This cog keeps the bot (in)sane"""

    def __init__(self, bot):
        self.bot = bot
        self.schizo_task.start()

        self.fconfig = toml.load("config.toml")

        self.unhinged = open("data/hanne.txt").read().split("\n")

    def cog_unload(self):
        self.schizo_task.cancel()

    async def be_silly(self):
        hannelore = await self.bot.fetch_user(721355984940957816)
        await hannelore.send(random.choice(self.unhinged))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Doing something silly")
        await self.be_silly()

    @tasks.loop(seconds=600.0)
    async def schizo_task(self):
        await self.be_silly()

    @schizo_task.before_loop
    async def before_schizo_task(self):
        print("Waiting for bot to be ready before being silly")
        await self.bot.wait_until_ready()
        print("Bot is ready. Enabling silly task")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if message.author.id == 721355984940957816:
                if random.randint(1, 100) <= 10:
                    await message.channel.send(random.choice(self.unhinged))


def setup(bot):
    print("Loading insanity ext")
    bot.add_cog(Schizo(bot))
