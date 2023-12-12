import datetime, asyncio, toml, random, disnake
from random import randint

from disnake.ext import commands, tasks
from better_profanity import profanity
from PIL import Image, ImageDraw, ImageFont

from .util_functions import *

profanity.load_censor_words(whitelist_words=["tit", "tits", "titties"])


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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:  # nobody cares if it's ourselves
            # Log any DMs that are not from the owner
            if (
                type(message.channel) == disnake.DMChannel
                or type(message.channel) == disnake.GroupChannel
            ) and message.author.id != self.bot.owner_id:
                owner = await self.bot.fetch_user(self.bot.owner_id)
                await owner.send(
                    f"DM from `{message.author.display_name}` ({message.author.id}): ```{message.content}```"
                )

            # Check for guild message outside owner's guilds
            elif type(message.channel) == disnake.TextChannel:
                if (
                    message.guild.id not in self.indexed_guilds
                ):  # Check if guild is indexed
                    if (
                        message.guild.owner.id != self.bot.owner_id
                    ):  # Check if owner is not in guild
                        self.indexed_guilds.append(
                            message.guild.id
                        )  # Add guild ID to list
                        owner = await self.bot.fetch_user(self.bot.owner_id)
                        await owner.send(
                            f"Message in guild `{message.guild.name}` (ID: {message.guild.id}) where owner is not present:\n"
                            f"From `{message.author.display_name}` ({message.author.id}): `{message.content}`"
                        )
                        await owner.send(
                            "Owner is: `" + message.guild.owner.mention + "`"
                        )

            # Code to bother hanne
            if message.author.id != self.bot.user.id:
                if message.author.id == 721355984940957816:
                    if random.randint(1, 100) <= 5:
                        await message.channel.send(random.choice(self.unhinged))
                    if random.randint(1, 500) < 100:
                        await self.be_silly()

            # Code to deal with "profanity"
            if profanity.contains_profanity(message.content):

                opt = randint(1,4)

                if opt == 1:
                    await message.add_reaction("😿")
                elif opt == 2:
                    await message.add_reaction("🤬")
                elif opt == 3:
                    await message.channel.send("stop it", file=disnake.File("images/dogegun.jpg"))
                elif opt == 4:
                    try:  # if we don't have permission to CAT, then
                        msg = "stop it"
                        new_text = message.author.display_name

                        censored = profanity.censor(message.content)

                        #await owner.send("It was censored to: `" + censored + "`")

                        self.make_bonk(new_text)

                        await message.channel.send(
                            msg, reference=message, file=disnake.File("bonk-s.png")
                        )
                        
                        os.remove("bonk-s.png")
                    except Exception as e:  # we just send a normal message
                        await message.channel.send("stop it", reference=message)
                        owner = await self.bot.fetch_user(self.bot.owner_id)
                        await owner.send("Error: `" + str(e) + "`")

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