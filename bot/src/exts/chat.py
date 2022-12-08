import shutil, os
import urllib

import requests
from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands

from .util_functions import *


@commands.slash_command()
async def crab(ctx):
    """🦀🦀🦀🦀🦀"""
    await ctx.response.send_message(
        "https://media.tenor.com/images/a16246936101a550918944740789de8a/tenor.gif",
    )


@commands.slash_command()
async def deadchat(ctx):
    """When the chat do be dead"""
    await ctx.response.send_message(
        "https://media.tenor.com/images/f799b7d7993b74a7852e1eaf2695d9d7/tenor.gif",
    )


@commands.slash_command()
async def xd(ctx):
    """😂😂😂😂😂"""
    await ctx.response.send_message(file=disnake.File("images/LMAO.jpg"))


@commands.slash_command()
async def kat(ctx):
    """*sad cat noises*"""
    await ctx.response.send_message(file=disnake.File("images/krying_kat.png"))


@commands.slash_command()
async def yea(ctx):
    """it do be like that"""
    await ctx.response.send_message(file=disnake.File("images/yeah.png"))


@commands.slash_command()
async def no(ctx):
    """it do not be like that"""
    await ctx.response.send_message(file=disnake.File("images/no.png"))


@commands.slash_command()
async def stoptalking(ctx):
    """just do."""
    await ctx.response.send_message(file=disnake.File("images/stop_talking.png"))


@commands.slash_command()
async def forkbomb(ctx):
    """rip to myself"""
    await ctx.response.send_message(file=disnake.File("images/forkbomb.jpg"))


@commands.slash_command()
async def permit(ctx):
    """go right ahead."""
    await ctx.response.send_message(file=disnake.File("images/permit_crab.jpg"))


@commands.slash_command()
async def whenthe(ctx):
    """use this when the"""
    await ctx.response.send_message(
        "https://cdn.discordapp.com/attachments/732599669867413505/921838252275695686/7Vcj8V5vrrN7G71g.mp4"
    )


@commands.slash_command()
async def floppa(ctx, *, emote=""):
    """floppa things"""
    if emote == "":
        files = os.listdir("images/floppa")
        await ctx.response.send_message(
            file=disnake.File("images/floppa/" + random.choice(files))
        )
    else:
        if os.path.exists("images/floppa/" + emote + ".png"):
            await ctx.response.send_message(
                file=disnake.File("images/floppa/" + emote + ".png")
            )
        else:
            await ctx.response.send_message(
                "No such floppa: `" + emote + "`"
            )


@commands.slash_command()
async def lahmoji(ctx, *, emote=""):
    """Lah emote pog"""
    if emote == "":
        files = os.listdir("images/lahcollection")
        await ctx.response.send_message(
            file=disnake.File("images/lahcollection/" + random.choice(files))
        )
    else:
        for ext in [".jpg", ".png", ".gif"]:
            if os.path.exists("images/lahcollection/" + emote + ext):
                await ctx.response.send_message(
                    file=disnake.File("images/lahcollection/" + emote + ext)
                )
                return

        await ctx.response.send_message(
            "No such lahmoji: `" + emote + "`"
        )


@commands.slash_command()
async def catpic(ctx):
    """Get a cat pic"""
    r = requests.get("https://cataas.com/cat", allow_redirects=True)
    name = "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
    open(name, "wb").write(r.content)
    await ctx.response.send_message(file=disnake.File(name))


@commands.slash_command()
async def catgif(ctx):
    """Everybody needs cat gifs in their lifes"""
    r = requests.get("https://cataas.com/cat/gif", allow_redirects=True)
    name = "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".gif"
    open(name, "wb").write(r.content)
    await ctx.response.send_message(file=disnake.File(name))


@commands.slash_command()
async def catsays(ctx, *, msg):
    """Cat can speak!"""
    r = requests.get(
        "https://cataas.com/cat/says/" + urllib.parse.quote(msg.encode("utf-8")),
        allow_redirects=True,
    )
    name = "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
    open(name, "wb").write(r.content)
    await ctx.response.send_message(file=disnake.File(name))


@commands.slash_command()
async def poll(ctx, *, info=None):
    """Make a poll with numeric options"""
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    if not info:
        await ctx.response.send_message(
            "Please format your poll like: `-poll question,option1,option2, ... `"
        )
    else:
        if not "," in info:
            await ctx.response.send_message(
                "Please format your poll like: `-poll question,option1,option2, ... `"
            )
        else:
            things = info.split(",")
            embed = disnake.Embed(
                color=disnake.Colour.blurple(),
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
                msg = await ctx.response.send_message(embed=embed)
                eid = 0
                for _ in things:
                    await msg.add_reaction(emojis[eid])
                    eid += 1
            else:
                await ctx.response.send_message("Too many choices :(")


# TODO: get this working again?
"""
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
            msg, reference=message, file=disnake.File("bonk-s.png")
        )
        os.remove("bonk-s.png")
"""


def setup(bot):
    print("Loading chat extension")
    # crab,deadchat,xd,kat,yea,no,stoptalking,forkbomb,permit,whenthe,floppa,lahmoji,catpic,catgif,catsays,poll
    bot.add_slash_command(crab)
    bot.add_slash_command(deadchat)
    bot.add_slash_command(xd)
    bot.add_slash_command(kat)
    bot.add_slash_command(yea)
    bot.add_slash_command(no)
    bot.add_slash_command(stoptalking)
    bot.add_slash_command(forkbomb)
    bot.add_slash_command(permit)
    bot.add_slash_command(whenthe)
    bot.add_slash_command(floppa)
    bot.add_slash_command(lahmoji)
    bot.add_slash_command(catpic)
    bot.add_slash_command(catgif)
    bot.add_slash_command(catsays)
    bot.add_slash_command(poll)
    print("Done.")
