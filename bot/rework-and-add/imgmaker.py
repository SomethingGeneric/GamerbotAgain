from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

from util_functions import *


# Hopefully we'll never need logging here
# (but who knows)

# Start memes
class ImageMaker(commands.Cog):
    """Haha image manipulation go brr"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def figlet(self, ctx, *, text):
        """Fun text art :)"""
        try:
            out = await run_command_shell("figlet " + text.strip())
            if len(out) < 1994:
                await ctx.send("```\n " + str(out) + "```")
            else:
                link = await paste(out)
                await ctx.send(
                    ctx.message.author.mention
                    + ", the figlet output is too long, so here's a link: "
                    + link
                )
        except Exception as e:
            await ctx.send(
                embed=err_msg("Error", "Had an issue running figlet: `" + str(e) + "`")
            )
            syslog.log(
                "Memes-Important", "Had an issue running figlet: `" + str(e) + "`"
            )

    @commands.command()
    async def onceagain(self, ctx, *, text="for your financial support"):
        """What is bernie's campaign this time?"""
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
        await ctx.send(
            f"{ctx.message.author.mention} is once again asking...",
            file=discord.File("bernie-gen.png"),
            reference=ctx.message,
        )
        os.remove("bernie-gen.png")

    @commands.command()
    async def bonk(self, ctx, *, text=""):
        """Bonk a buddy"""

        if text == "":
            text = ctx.message.author.mention

        new_text = text.strip()
        extra = ""

        if "<@!" in new_text or "<@" in new_text:
            try:
                pid = new_text.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person is not None:
                    new_text = person.display_name
                    extra = "Get bonked, " + person.mention
                else:
                    await ctx.send("Had trouble getting a user from: " + text)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")

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
            await ctx.send(extra, file=discord.File("bonk-s.png"))
            os.remove("bonk-s.png")
        else:
            await ctx.send(file=discord.File("images/bonk.png"))

    @commands.command()
    async def space(self, ctx, *, who):
        """Send ur friends to space lol"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person is not None:
                    pfp = str(person.display_avatar.url)
                    os.system("wget " + pfp + " -O prof.webp")
                    bg = Image.open("images/spacex.jpg")
                    fg = Image.open("prof.webp")
                    fg = fg.resize((128, 128))
                    bg.paste(fg, (620, 0), fg.convert("RGBA"))
                    bg.save("temp.png")
                    await ctx.send(
                        ":rocket::sparkles: See ya later "
                        + person.mention
                        + " :sparkles::rocket:",
                        file=discord.File("temp.png"),
                    )
                    os.remove("temp.png")
                    os.remove("prof.webp")
                else:
                    await ctx.send("Had trouble getting a user from: " + who)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")
        else:
            await ctx.send(
                ctx.message.author.mention + ", who are you sending to space?"
            )

    @commands.command()
    async def pfp(self, ctx, *, who):
        """Yoink a cool PFP from a user"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person is not None:
                    pfp = str(person.display_avatar.url)
                    await ctx.send(ctx.message.author.mention + " here: " + pfp)
                else:
                    await ctx.send("Had trouble getting a user from: " + who)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")
        else:
            await ctx.send(ctx.message.author.mention + ", that ain't a user.")


# End memes
async def setup(bot):
    await bot.add_cog(ImageMaker(bot))
