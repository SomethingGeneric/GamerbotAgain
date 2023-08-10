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


line_before
new_code
line_after