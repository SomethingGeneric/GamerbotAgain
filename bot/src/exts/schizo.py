import datetime, asyncio, toml, random, disnake, requests, json, aiohttp
from random import randint

from disnake.ext import commands, tasks
from better_profanity import profanity
from PIL import Image, ImageDraw, ImageFont

from .util_functions import *

profanity.load_censor_words(
    whitelist_words=["tit", "tits", "titties", "god", "lmao", "spac"]
)


class Schizo(commands.Cog):
    """This cog keeps the bot (in)sane"""

    def __init__(self, bot):
        self.bot = bot
        self.schizo_task.start()

        self.fconfig = toml.load("config.toml")

        self.unhinged = open("data/hanne.txt").read().split("\n")

        self.indexed_guilds = []

    def cog_unload(self):
        self.schizo_task.cancel()

    async def be_silly(self):
        try:
            hannelore = await self.bot.fetch_user(721355984940957816)
            await hannelore.send(random.choice(self.unhinged))
        except Exception as e:
            print(f"Failed to send silly message: {str(e)}")

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

    @commands.slash_command()
    async def dm(self, inter, *, text: str):
        """Make the bot say something"""
        await inter.response.defer()

        if inter.author.id != self.bot.owner_id:
            await inter.send("You can't do that!")
            return

        new_text = text.strip()

        if "<@!" in new_text or "<@" in new_text:
            try:
                pid = new_text.split(">")[0].replace("<@!", "").replace("<@", "")
                await inter.send("Sending to: " + new_text)
                person = await inter.bot.fetch_user(int(pid))

                if person is not None:
                    await person.send(text.split(">")[1])
                    await inter.send("Done.")
                else:
                    await inter.send("Had trouble getting a user from: " + new_text)
            except Exception as e:
                await inter.send("Had trouble getting a user from: " + new_text)
                await inter.send("```" + str(e) + "```")

    async def fetch_data(self, url, data):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, json=data)
            return response

    def make_bonk(self, new_text):
        img = Image.open("images/bonk.png")

        arial_font = ImageFont.truetype("fonts/arial.ttf", (50 - len(str(new_text))))
        draw = ImageDraw.Draw(img)
        draw.text(
            (525 - len(str(new_text)) * 5, 300),
            str(new_text),
            (0, 0, 0),
            font=arial_font,
        )
        img.save("bonk-s.png")


def setup(bot):
    print("Loading insanity ext")
    bot.add_cog(Schizo(bot))
