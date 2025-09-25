from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands
from pyfiglet import Figlet

import re

from .util_functions import *


class ImageMaker(commands.Cog):
    """Dynamic image funny stuff"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def figlet(self, inter, *, text):
        """Fun text art :)"""
        await inter.response.defer()
        try:
            f = Figlet()
            ascii_art = f.renderText(text)
            await inter.send(f"```\n{ascii_art}\n```")
        except Exception as e:
            await inter.send(
                embed=err_msg("Error", "Had an issue running figlet: `" + str(e) + "`")
            )

    def _calculate_font_size(self, text, base_size=50, min_size=16):
        """
        Calculate font size based on text length with improved algorithm.
        Less aggressive than the original (50 - len(text)) approach.
        """
        text_len = len(str(text))
        if text_len <= 10:
            return base_size
        else:
            # Gentler reduction: 0.6 per character after the first 10
            reduction = int((text_len - 10) * 0.6)
            return max(base_size - reduction, min_size)

    @commands.slash_command()
    async def onceagain(self, inter, *, text="for your financial support"):
        """What is bernie's campaign this time?"""
        await inter.response.defer()
        new_text = text

        img = Image.open("images/bernie.jpg")
        font_size = self._calculate_font_size(new_text)
        arial_font = ImageFont.truetype("fonts/arial.ttf", font_size)
        draw = ImageDraw.Draw(img)
        draw.text(
            (130, 585),  # xy
            str(new_text),  # text
            "white",  # fill
            font=arial_font,  # font
        )
        img.save("bernie-gen.png")
        await inter.send(
            f"{inter.author.mention} is once again asking...",
            file=disnake.File("bernie-gen.png"),
        )
        os.remove("bernie-gen.png")

    @commands.slash_command()
    async def bugs(self, inter, *, text_one: str, text_two: str):
        """Bugs bunny generator"""
        await inter.response.defer()
        try:
            scale_fac = 2

            avg_len = int(len(text_one) + len(text_two) / 2)
            avg_len = int(avg_len / scale_fac)

            img = Image.open("images/bugs.png")
            arial_font = ImageFont.truetype("fonts/arial.ttf", (40 - avg_len))

            draw = ImageDraw.Draw(img)

            draw.text(
                (50, 100),  # xy
                str(text_one),  # text
                "white",  # fill
                font=arial_font,  # font
            )

            draw.text(
                (50, 300),  # xy
                str(text_two),  # text
                "white",  # fill
                font=arial_font,  # font
            )

            img.save("bugs-gen.png")
            await inter.send(file=disnake.File("bugs-gen.png"))
            os.remove("bugs-gen.png")
        except Exception as e:
            await inter.send("Whoops: `" + str(e) + "`.")

    @commands.slash_command()
    async def bonk(self, inter, *, text=""):
        """Bonk a buddy"""
        await inter.response.defer()
        try:
            if text == "":
                text = inter.author.mention

            new_text = text.strip()
            extra = ""

            if "<@!" in new_text or "<@" in new_text:
                try:
                    pid = new_text.replace("<@!", "").replace("<@", "").replace(">", "")
                    person = await inter.bot.fetch_user(int(pid))
                    if person is not None:
                        new_text = person.display_name
                        extra = "Get bonked, " + person.mention
                    else:
                        await inter.send("Had trouble getting a user from: " + text)
                except Exception as e:
                    await inter.send("We had a failure: `" + str(e) + "`")

            if new_text != "":
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
                await inter.send(extra, file=disnake.File("bonk-s.png"))
                os.remove("bonk-s.png")
            else:
                await inter.send(file=disnake.File("images/bonk.png"))
        except Exception as e:
            await inter.send(f"Error: ```{str(e)}```")

    @commands.slash_command()
    async def space(self, inter, *, who):
        """Send ur friends to space lol"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await inter.bot.fetch_user(int(pid))
                if person is not None:
                    pfp = str(person.display_avatar.url)
                    os.system("wget " + pfp + " -O prof.webp")
                    bg = Image.open("images/spacex.jpg")
                    fg = Image.open("prof.webp")
                    fg = fg.resize((128, 128))
                    bg.paste(fg, (620, 0), fg.convert("RGBA"))
                    bg.save("temp.png")
                    await inter.send(
                        ":rocket::sparkles: See ya later "
                        + person.mention
                        + " :sparkles::rocket:",
                        file=disnake.File("temp.png"),
                    )
                    os.remove("temp.png")
                    os.remove("prof.webp")
                else:
                    await inter.send("Had trouble getting a user from: " + who)
            except Exception as e:
                await inter.send("We had a failure: `" + str(e) + "`")
        else:
            await inter.send(inter.author.mention + ", who are you sending to space?")

    @commands.slash_command()
    async def pfp(self, inter, *, who):
        """Yoink a cool PFP from a user"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await inter.bot.fetch_user(int(pid))
                if person is not None:
                    pfp = str(person.display_avatar.url)
                    await inter.send(inter.author.mention + " here: " + pfp)
                else:
                    await inter.send("Had trouble getting a user from: " + who)
            except Exception as e:
                await inter.send("We had a failure: `" + str(e) + "`")
        else:
            await inter.send(inter.author.mention + ", that ain't a user.")

    @commands.slash_command()
    async def forkbomb(self, inter, *, text=""):
        """rip to myself"""
        if text == "":
            await inter.send(file=disnake.File("images/forkbomb.jpg"))
        else:
            await inter.response.defer()
            new_text = text
            img = Image.open("images/forkbomb-template.jpg")
            arial_font = ImageFont.truetype(
                "fonts/arial.ttf", (50 - len(str(new_text)))
            )
            draw = ImageDraw.Draw(img)
            draw.text(
                (20, 160),
                str(new_text),
                (0, 0, 0),
                font=arial_font,
            )
            img.save("fb-s.jpg")
            await inter.send(file=disnake.File("fb-s.jpg"))
            os.remove("fb-s.jpg")


def setup(bot):
    print("Loading imgmaker extension")
    bot.add_cog(ImageMaker(bot))
