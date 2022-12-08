from disnake.ext import commands
from mastodon import Mastodon
from random_word import RandomWords
from time import sleep
from random import randint
import os, binascii
import toml
import re, yaml

from .util_functions import *

# /gb-data

volpath = "/gb-data"
ccredpath = "tootclientcred.secret"
ucredpath = "tootusercred.secret"
acf = f"{volpath}/mastodon_linked.toml"
conf_f = f"{volpath}/mastodon_temp.toml"

with open("conf.yml", "r") as stream:
    try:
        fconfig = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

url = fconfig["MASTODON_URL"]
email = fconfig["MASTODON_EMAIL"]
passw = fconfig["MASTODON_PASSWORD"]


@commands.slash_command()
async def fediconfirm(inter, code=""):
    try:
        pending = {}
        if os.path.exists(conf_f):
            pending = toml.load(conf_f)

        if str(inter.author.id) in pending.keys():
            # we have a conf in progress
            person = pending[str(inter.author.id)]
            if person["code"] == code:

                # commit association to acf
                if os.path.exists(acf):
                    data = toml.load(acf)
                else:
                    data = {}

                username = person["username"]

                if username[0] != "@":
                    username = "@" + username

                data[str(inter.author.id)] = username
                f = open(acf, "w")
                toml.dump(data, f)
                f.close()

                # remove user info from conf_f
                pending.pop(str(inter.author.id))
                f = open(conf_f, "w")
                toml.dump(pending, f)
                f.close()

                await inter.send("Thanks! I'll keep track of that.")
            else:
                await inter.send("Wrong confirmation code")
        else:
            await inter.send("You need to run `-linkfediverse` first!")

    except Exception as e:
        await inter.send(f"Error: ```{str(e)}```")


@commands.slash_command()
async def linkfediverse(inter, username):
    """Tell gamerbot of your mastodon handle"""
    try:
        # todo validate username
        if not re.search(r"^[@]\w+[@]\w+\.\w+", username):
            await inter.send("That doesn't look like a mastodon username.")
            return

        person = {
            "code": str(binascii.b2a_hex(os.urandom(15)).decode("utf-8")),
            "username": username,
        }

        pending = {}
        if os.path.exists(conf_f):
            pending = toml.load(conf_f)

        pending[str(inter.author.id)] = person

        f = open(conf_f, "w")
        toml.dump(pending, f)
        f.close()

        if not os.path.isfile(f"{volpath}/{ccredpath}"):
            r = RandomWords()
            w = r.get_random_word()
            Mastodon.create_app(
                f"gamerthebot-{w}-{str(randint(1, 10))}",
                api_base_url=url,
                to_file=f"{volpath}/{ccredpath}",
            )

        mastodon = Mastodon(client_id=f"{volpath}/{ccredpath}")

        mastodon.log_in(
            email,
            passw,
            to_file=f"{volpath}/{ucredpath}",
        )

        mastodon.status_post(
            f"{username}, your code: {person['code']}", visibility="direct"
        )

        await inter.send(
            "I've sent your mastodon account a confirmation code. Run `-fediconfirm <code>` to finish the link.",
        )

    except Exception as e:
        await inter.send(f"Error: ```{str(e)}```")


@commands.slash_command()
async def toot(inter, *, text=""):
    """Send a post out to the fediverse. (Add your handle in the form of a mention)"""

    try:
        has_attach = False

        # TODO: Figure out how to do images w/ slash??
        """
        fns = []
        if (
            inter.message.attachments is not None
            and len(inter.message.attachments) != 0
        ):
            if len(inter.message.attachments) > 3:  # 0,1,2,3 = 4 total
                await inter.send("Too many attachments")
                return

            has_attach = True
            for attachment in inter.message.attachments:
                fns.append(attachment.filename)
                await attachment.save(attachment.filename)

        """

        if not os.path.isfile(f"{volpath}/{ccredpath}"):
            r = RandomWords()
            w = r.get_random_word()
            Mastodon.create_app(
                f"gamerthebot-{w}-{str(randint(1, 10))}",
                api_base_url=url,
                to_file=f"{volpath}/{ccredpath}",
            )

        if not has_attach and text == "":
            await inter.send("Please include an image and/or some text.")
            return

        await inter.send(
            f"Going to post `{text}`, this could take a sec.",
        )

        mastodon = Mastodon(client_id=f"{volpath}/{ccredpath}")

        mastodon.log_in(
            email,
            passw,
            to_file=f"{volpath}/{ucredpath}",
        )

        un = inter.author.name
        dc = inter.author.discriminator

        if os.path.exists(acf):
            data = toml.load(acf)
        else:
            data = {}

        cred = f"{un}#{str(dc)}"

        if str(inter.author.id) in data.keys():
            cred = data[str(inter.author.id)]

        if has_attach:
            med = []
            for fn in fns:
                med.append(mastodon.media_post(fn))
                sleep(4)
            res = mastodon.status_post(f"{text} - {cred}", media_ids=med)
        else:
            res = mastodon.toot(f"{text} - {cred}")

        with open(f"{volpath}/post-log.txt", "a+") as f:
            f.write(f"User {cred} posted: '{text}'\n")

        await inter.send(f"See your post here: {res['url']}")

        if has_attach:
            for fn in fns:
                os.remove(fn)

    except Exception as e:
        await inter.send(f"A thing happened: ```{str(e)}```")


@disnake.ext.commands.is_owner()
@commands.slash_command(name="post-log")
async def post_log(inter):
    """Don't even worry about it"""
    with open(f"{volpath}/post-log.txt") as f:
        raw_log = f.read()
    msg = f"```{raw_log}```"
    if len(msg) > 400:
        msg = pastef(f"{volpath}/post-log.txt")
    await inter.send(msg)


def setup(bot):
    print("Loading Social extension")
    bot.add_slash_command(fediconfirm)
    bot.add_slash_command(linkfediverse)
    bot.add_slash_command(toot)
    bot.add_slash_command(post_log)
    print("Done.")
