import shutil, os
import urllib

import requests
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

from util_functions import *


class Chat(commands.Cog):
    """Images for use in chat"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crab(self, ctx):
        """🦀🦀🦀🦀🦀"""
        await ctx.send(
            "https://media.tenor.com/images/a16246936101a550918944740789de8a/tenor.gif",
        )

    @commands.command()
    async def deadchat(self, ctx):
        await ctx.send(
            "https://media.tenor.com/images/f799b7d7993b74a7852e1eaf2695d9d7/tenor.gif",
        )

    @commands.command()
    async def xd(self, ctx):
        """😂😂😂😂😂"""
        await ctx.send(file=discord.File("images/LMAO.jpg"))

    @commands.command()
    async def kat(self, ctx):
        """*sad cat noises*"""
        await ctx.send(file=discord.File("images/krying_kat.png"))

    @commands.command()
    async def yea(self, ctx):
        """it do be like that"""
        await ctx.send(file=discord.File("images/yeah.png"))

    @commands.command()
    async def no(self, ctx):
        """it do not be like that"""
        await ctx.send(file=discord.File("images/no.png"))

    @commands.command()
    async def stoptalking(self, ctx):
        """just do."""
        await ctx.send(file=discord.File("images/stop_talking.png"))

    @commands.command()
    async def forkbomb(self, ctx):
        """rip to myself"""
        await ctx.send(file=discord.File("images/forkbomb.jpg"))

    @commands.command()
    async def permit(self, ctx):
        """go right ahead."""
        await ctx.send(file=discord.File("images/permit_crab.jpg"))

    @commands.command()
    async def whenthe(self, ctx):
        """use this when the"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/732599669867413505/921838252275695686/7Vcj8V5vrrN7G71g.mp4"
        )

    @commands.command()
    async def floppa(self, ctx, *, emote=""):
        """floppa things"""
        if emote == "":
            files = os.listdir("images/floppa")
            await ctx.send(file=discord.File("images/floppa/" + random.choice(files)))
        else:
            if os.path.exists("images/floppa/" + emote + ".png"):
                await ctx.send(file=discord.File("images/floppa/" + emote + ".png"))
            else:
                await ctx.send("No such floppa: `" + emote + "`", reference=ctx.message)

    @commands.command()
    async def lahmoji(self, ctx, *, emote=""):
        if emote == "":
            files = os.listdir("images/lahcollection")
            await ctx.send(
                file=discord.File("images/lahcollection/" + random.choice(files))
            )
        else:
            for ext in [".jpg", ".png", ".gif"]:
                if os.path.exists("images/lahcollection/" + emote + ext):
                    await ctx.send(
                        file=discord.File("images/lahcollection/" + emote + ext)
                    )
                    return

            await ctx.send("No such lahmoji: `" + emote + "`", reference=ctx.message)

    @commands.command()
    async def catpic(self, ctx):
        r = requests.get("https://cataas.com/cat", allow_redirects=True)
        name = (
            "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
        )
        open(name, "wb").write(r.content)
        await ctx.send(file=discord.File(name))

    @commands.command()
    async def catgif(self, ctx):
        r = requests.get("https://cataas.com/cat/gif", allow_redirects=True)
        name = (
            "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".gif"
        )
        open(name, "wb").write(r.content)
        await ctx.send(file=discord.File(name))

    @commands.command()
    async def catsays(self, ctx, *, msg):
        r = requests.get(
            "https://cataas.com/cat/says/" + urllib.parse.quote(msg.encode("utf-8")),
            allow_redirects=True,
        )
        name = (
            "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
        )
        open(name, "wb").write(r.content)
        await ctx.send(file=discord.File(name))

    @commands.command()
    async def poll(self, ctx, *, info=None):
        """Make a poll with numeric options"""
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        if not info:
            await ctx.send(
                "Please format your poll like: `-poll question,option1,option2, ... `"
            )
        else:
            if not "," in info:
                await ctx.send(
                    "Please format your poll like: `-poll question,option1,option2, ... `"
                )
            else:
                things = info.split(",")
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title=f"Poll: {things[0]}",
                )
                things.pop(0)
                if len(things) < 10:
                    eid = 0
                    for choice in things:
                        embed.add_field(
                            name=f"{choice}", value=f"{emojis[eid]}", inline=False
                        )
                        eid += 1
                    embed.set_footer(text="Remember, count reactions-1 as total votes.")
                    msg = await ctx.send(embed=embed)
                    eid = 0
                    for _ in things:
                        await msg.add_reaction(emojis[eid])
                        eid += 1
                else:
                    await ctx.send("Too many choices :(")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "shut" in message.content and "the fuck up" in message.content:
            msg = "no u"

            if "shut the" in message.content:
                new_text = message.author.display_name
            else:
                new_text = message.content.split(" ")[1]
                pid = new_text.replace("<@!", "").replace("<@", "").replace(">", "")
                try:
                    person = await self.bot.fetch_user(int(pid))
                    if person is not None:
                        new_text = person.display_name
                        msg = "silence " + person.mention
                    else:
                        msg = ""
                except:
                    msg = "silence"
            img = Image.open("images/bonk.png")

            arial_font = ImageFont.truetype(
                "fonts/arial.ttf", (50 - len(str(new_text)))
            )
            draw = ImageDraw.Draw(img)
            draw.text(
                (525 - len(str(new_text)) * 5, 300),
                str(new_text),
                (0, 0, 0),
                font=arial_font,
            )
            img.save("bonk-s.png")
            await message.channel.send(
                msg, reference=message, file=discord.File("bonk-s.png")
            )
            os.remove("bonk-s.png")


async def setup(bot):
    await bot.add_cog(Chat(bot))
