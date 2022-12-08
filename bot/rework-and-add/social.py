from discord.ext import commands
from mastodon import Mastodon
from random_word import RandomWords
from time import sleep
from random import randint
import os, binascii
import toml
import re

from util_functions import *

# /gb-data


class Social(commands.Cog):
    """Funny social internet stuff"""

    def __init__(self, bot):
        self.bot = bot

        self.volpath = "/gb-data"
        self.ccredpath = "tootclientcred.secret"
        self.ucredpath = "tootusercred.secret"
        self.acf = f"{self.volpath}/mastodon_linked.toml"
        self.conf_f = f"{self.volpath}/mastodon_temp.toml"

    @commands.command()
    async def fediconfirm(self, ctx, code=""):
        try:
            pending = {}
            if os.path.exists(self.conf_f):
                pending = toml.load(self.conf_f)

            if str(ctx.message.author.id) in pending.keys():
                # we have a conf in progress
                person = pending[str(ctx.message.author.id)]
                if person["code"] == code:

                    # commit association to self.acf
                    if os.path.exists(self.acf):
                        data = toml.load(self.acf)
                    else:
                        data = {}

                    username = person["username"]

                    if username[0] != "@":
                        username = "@" + username

                    data[str(ctx.message.author.id)] = username
                    f = open(self.acf, "w")
                    toml.dump(data, f)
                    f.close()

                    # remove user info from self.conf_f
                    pending.pop(str(ctx.message.author.id))
                    f = open(self.conf_f, "w")
                    toml.dump(pending, f)
                    f.close()

                    await ctx.send(
                        "Thanks! I'll keep track of that.", reference=ctx.message
                    )
                else:
                    await ctx.send("Wrong confirmation code", reference=ctx.message)
            else:
                await ctx.send(
                    "You need to run `-linkfediverse` first!", reference=ctx.message
                )

        except Exception as e:
            await ctx.send(f"Error: ```{str(e)}```", reference=ctx.message)

    @commands.command()
    async def linkfediverse(self, ctx, username):
        """Tell gamerbot of your mastodon handle"""
        try:
            # todo validate username
            if not re.search(r"^[@]\w+[@]\w+\.\w+", username):
                await ctx.send(
                    "That doesn't look like a mastodon username.", reference=ctx.message
                )
                return

            person = {
                "code": str(binascii.b2a_hex(os.urandom(15)).decode("utf-8")),
                "username": username,
            }

            pending = {}
            if os.path.exists(self.conf_f):
                pending = toml.load(self.conf_f)

            pending[str(ctx.message.author.id)] = person

            f = open(self.conf_f, "w")
            toml.dump(pending, f)
            f.close()

            if not os.path.isfile(f"{self.volpath}/{self.ccredpath}"):
                r = RandomWords()
                w = r.get_random_word()
                Mastodon.create_app(
                    f"gamerthebot-{w}-{str(randint(1, 10))}",
                    api_base_url=url,
                    to_file=f"{self.volpath}/{self.ccredpath}",
                )

            mastodon = Mastodon(client_id=f"{self.volpath}/{self.ccredpath}")

            url = os.environ.get("MASTODON_URL")
            email = os.environ.get("MASTODON_EMAIL")
            passw = os.environ.get("MASTODON_PASSWORD")

            mastodon.log_in(
                email,
                passw,
                to_file=f"{self.volpath}/{self.ucredpath}",
            )

            mastodon.status_post(
                f"{username}, your code: {person['code']}", visibility="direct"
            )

            await ctx.send(
                "I've sent your mastodon account a confirmation code. Run `-fediconfirm <code>` to finish the link.",
                reference=ctx.message,
            )

        except Exception as e:
            await ctx.send(f"Error: ```{str(e)}```", reference=ctx.message)

    @commands.command()
    async def toot(self, ctx, *, text=""):
        """Send a post out to the fediverse. (Add your handle in the form of a mention)"""

        try:
            has_attach = False
            fns = []
            if (
                ctx.message.attachments is not None
                and len(ctx.message.attachments) != 0
            ):
                if len(ctx.message.attachments) > 3:  # 0,1,2,3 = 4 total
                    await ctx.send("Too many attachments")
                    return

                has_attach = True
                for attachment in ctx.message.attachments:
                    fns.append(attachment.filename)
                    await attachment.save(attachment.filename)

            url = os.environ.get("MASTODON_URL")
            email = os.environ.get("MASTODON_EMAIL")
            passw = os.environ.get("MASTODON_PASSWORD")

            if not os.path.isfile(f"{self.volpath}/{self.ccredpath}"):
                r = RandomWords()
                w = r.get_random_word()
                Mastodon.create_app(
                    f"gamerthebot-{w}-{str(randint(1, 10))}",
                    api_base_url=url,
                    to_file=f"{self.volpath}/{self.ccredpath}",
                )

            if not has_attach and text == "":
                await ctx.send(
                    "Please include an image and/or some text.", reference=ctx.message
                )
                return

            await ctx.send(
                f"Going to post `{text}`, this could take a sec.",
                reference=ctx.message,
            )

            mastodon = Mastodon(client_id=f"{self.volpath}/{self.ccredpath}")

            mastodon.log_in(
                email,
                passw,
                to_file=f"{self.volpath}/{self.ucredpath}",
            )

            un = ctx.message.author.name
            dc = ctx.message.author.discriminator

            if os.path.exists(self.acf):
                data = toml.load(self.acf)
            else:
                data = {}

            cred = f"{un}#{str(dc)}"

            if str(ctx.message.author.id) in data.keys():
                cred = data[str(ctx.message.author.id)]

            if has_attach:
                med = []
                for fn in fns:
                    med.append(mastodon.media_post(fn))
                    sleep(4)
                res = mastodon.status_post(f"{text} - {cred}", media_ids=med)
            else:
                res = mastodon.toot(f"{text} - {cred}")

            with open(f"{self.volpath}/post-log.txt", "a+") as f:
                f.write(f"User {cred} posted: '{text}'\n")

            await ctx.send(f"See your post here: {res['url']}", reference=ctx.message)

            if has_attach:
                for fn in fns:
                    os.remove(fn)

        except Exception as e:
            await ctx.send(f"A thing happened: ```{str(e)}```", reference=ctx.message)

    @commands.command()
    async def post_log(self, ctx):
        """Don't even worry about it"""
        if ctx.message.author.id == OWNER_ID:
            with open(f"{self.volpath}/post-log.txt") as f:
                raw_log = f.read()
            msg = f"```{raw_log}```"
            if len(msg) > 400:
                msg = pastef(f"{self.volpath}/post-log.txt")
            await ctx.send(msg, reference=ctx.message)
        else:
            await ctx.send(wrong_perms("post_log"))


async def setup(bot):
    await bot.add_cog(Social(bot))
