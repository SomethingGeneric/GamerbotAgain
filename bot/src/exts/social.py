from disnake.ext import commands
from mastodon import Mastodon
from random_word import RandomWords
from time import sleep
from random import randint
import os, binascii
import toml
import re, yaml, asyncio

from .util_functions import *

url = config["mastodon_url"]
email = config["mastodon_email"]
passw = config["mastodon_password"]
volpath = config["volpath"]

ccredpath = "tootclientcred.secret"
ucredpath = "tootusercred.secret"
acf = f"{volpath}/mastodon_linked.toml"
conf_f = f"{volpath}/mastodon_temp.toml"

class Social(commands.Cog):
    """Fediverse stuff"""

    def __init__(self, bot):
        self.bot = bot

    # Rest of the class code...

def setup(bot):
    print("Loading Social extension")
    bot.add_cog(Social(bot))
line_after