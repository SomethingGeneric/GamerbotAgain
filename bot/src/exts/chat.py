import shutil, os
import urllib

import requests
from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands

from .util_functions import *


class Chat(commands.Cog):
    """Stuff for the chat... Duh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def crab(self, inter):
        """🦀🦀🦀🦀🦀"""
        await inter.send(
            "https://media.tenor.com/images/a16246936101a550918944740789de8a/tenor.gif",
        )

    @commands.slash_command()
    async def deadchat(self, inter):
        """When the chat do be dead"""
        await inter.send(
            "https://media.tenor.com/images/f799b7d7993b74a7852e1eaf2695d9d7/tenor.gif",
        )

    @commands.slash_command()
    async def xd(self, inter):
        """😂😂😂😂😂"""
        await inter.send(file=disnake.File("images/LMAO.jpg"))

    @commands.slash_command()
    async def kat(self, inter):
        """*sad cat noises*"""
        await inter.send(file=disnake.File("images/krying_kat.png"))

    @commands.slash_command()
    async def yea(self, inter):
        """it do be like that"""
        await inter.send(file=disnake.File("images/yeah.png"))

    @commands.slash_command()
    async def no(self, inter):
        """it do not be like that"""
        await inter.send(file=disnake.File("images/no.png"))

    @commands.slash_command()
    async def stoptalking(self, inter):
        """just do."""
        await inter.send(file=disnake.File("images/stop_talking.png"))

    @commands.slash_command()
    async def forkbomb(self, inter):
        """rip to myself"""
        await inter.send(file=disnake.File("images/forkbomb.jpg"))

    @commands.slash_command()
    async def permit(self, inter):
        """go right ahead."""
        await inter.send(file=disnake.File("images/permit_crab.jpg"))

    @commands.slash_command()
    async def whenthe(self, inter):
        """use this when the"""
        await inter.send(
            "https://cdn.discordapp.com/attachments/732599669867413505/921838252275695686/7Vcj8V5vrrN7G71g.mp4"
        )

    @commands.slash_command()
    async def floppa(self, inter, *, emote=""):
        """floppa things"""
        if emote == "":
            files = os.listdir("images/floppa")
            await inter.send(file=disnake.File("images/floppa/" + random.choice(files)))
        else:
            if os.path.exists("images/floppa/" + emote + ".png"):
                await inter.send(file=disnake.File("images/floppa/" + emote + ".png"))
            else:
                await inter.send("No such floppa: `" + emote + "`")

    @commands.slash_command()
    async def lahmoji(self, inter, *, emote=""):
        """Lah emote pog"""
        if emote == "":
            files = os.listdir("images/lahcollection")
            await inter.send(
                file=disnake.File("images/lahcollection/" + random.choice(files))
            )
        else:
            for ext in [".jpg", ".png", ".gif"]:
                if os.path.exists("images/lahcollection/" + emote + ext):
                    await inter.send(
                        file=disnake.File("images/lahcollection/" + emote + ext)
                    )
                    return

            await inter.send("No such lahmoji: `" + emote + "`")

    # @commands.slash_command()
    # async def catpic(self, inter):
    #     """Get a cat pic"""
    #     r = requests.get("https://cataas.com/cat", allow_redirects=True)
    #     name = (
    #         "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
    #     )
    #     open(name, "wb").write(r.content)
    #     await inter.send(file=disnake.File(name))

    # @commands.slash_command()
    # async def catgif(self, inter):
    #     """Everybody needs cat gifs in their lifes"""
    #     r = requests.get("https://cataas.com/cat/gif", allow_redirects=True)
    #     name = (
    #         "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".gif"
    #     )
    #     open(name, "wb").write(r.content)
    #     await inter.send(file=disnake.File(name))

    # @commands.slash_command()
    # async def catsays(self, inter, *, msg):
    #     """Cat can speak!"""
    #     r = requests.get(
    #         "https://cataas.com/cat/says/" + urllib.parse.quote(msg.encode("utf-8")),
    #         allow_redirects=True,
    #     )
    #     name = (
    #         "".join(random.sample(string.ascii_lowercase + string.digits, 5)) + ".jpeg"
    #     )
    #     open(name, "wb").write(r.content)
    #     await inter.send(file=disnake.File(name))

    @commands.slash_command()
    async def poll(self, inter, *, info=None):
        """Make a poll with numeric options"""
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        if not info:
            await inter.send(
                "Please format your poll like: `-poll question,option1,option2, ... `"
            )
        else:
            if not "," in info:
                await inter.send(
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
                    msg = await inter.send(embed=embed)
                    eid = 0
                    for _ in things:
                        await msg.add_reaction(emojis[eid])
                        eid += 1
                else:
                    await inter.send("Too many choices :(")

    @commands.slash_command()
    async def dm(self, inter, *, text: str):
        """Make the bot say something"""

        if inter.author.id != self.bot.owner_id:
            await inter.send("You can't do that!")
            return

        new_text = text.strip()

        if "<@!" in new_text or "<@" in new_text:
            try:
                pid = new_text.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await inter.bot.fetch_user(int(pid))

                if person is not None:
                    await person.send(new_text.split(">")[1])
                    await inter.send("Done.")
                else:
                    await inter.send("Had trouble getting a user from: " + text)
            except Exception as e:
                await inter.send("Had trouble getting a user from: " + text)
                print(e)

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


def setup(bot):
    print("Adding Chat cog")
    bot.add_cog(Chat(bot))
