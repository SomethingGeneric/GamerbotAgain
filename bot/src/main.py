import disnake
import datetime, os, re, toml, pytz
from disnake.ext import commands

config = toml.load("config.toml")

intents = disnake.Intents().default()

bot = commands.InteractionBot(
    status=disnake.Status.online,
    intents=intents,
    # command_sync_flags=command_sync_flags,
    # sync_commands_debug=True
)

user_timezones = {}

error = ""
load_error = False

skip_exts = []

if config["skip_ext"] != "":
    if "," in config["skip_ext"]:
        skip_exts = config["skip_ext"].split(",")
    else:
        skip_exts = [config["skip_ext"]]

for fn in os.listdir("src/exts"):
    if (
        "util_functions" not in fn
        and "channel_state" not in fn
        and fn.replace(".py", "") not in skip_exts
        and not os.path.isdir(f"src/exts/{fn}")
    ):
        try:
            bot.load_extension(f"src.exts.{fn.replace('.py','')}")
        except Exception as e:
            error += f"Error trying to load extension `{fn}`: ```{str(e)}```\n\n"
            load_error = True


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} guilds, serving {len(bot.users)} users")
    if load_error:
        print(error)
