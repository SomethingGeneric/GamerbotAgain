from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands

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
            out = await run_command_shell("figlet " + text.strip())
            if len(out) < 1994:
                await inter.send("```\n " + str(out) + "```")
            else:
                link = await paste(out)
                await inter.send(
                    inter.author.mention
                    + ", the figlet output is too long, so here's a link: "
                    + link
                )
        except Exception as e:
            await inter.send(
                embed=err_msg("Error", "Had an issue running figlet: `" + str(e) + "`")
            )
            syslog.log(
                "Memes-Important", "Had an issue running figlet: `" + str(e) + "`"
            )

    @commands.slash_command()
    async def onceagain(self, inter, *, text="for your financial support"):
        """What is bernie's campaign this time?"""
        await inter.response.defer()
        new_text = text

        img = Image.open("images/bernie.jpg")
        arial_font = ImageFont.truetype("fonts/arial.ttf", (50 - len(str(new_text))))
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


def setup(bot):
    print("Loading imgmaker extension")
    bot.add_cog(ImageMaker(bot))
