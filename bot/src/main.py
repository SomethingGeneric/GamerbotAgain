import disnake
import yaml, datetime, os
from disnake.ext import commands

with open("conf.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

intents = disnake.Intents().default()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.members = True

# command_sync_flags = commands.CommandSyncFlags.default()
# command_sync_flags.sync_commands_debug = True

bot = commands.InteractionBot(
    status=disnake.Status.online,
    intents=intents,
    # command_sync_flags=command_sync_flags,
    # sync_commands_debug=True
)

error = ""
load_error = False

skip_exts = []

if config["SKIP_EXT"] != "":
    if "," in config["SKIP_EXT"]:
        skip_exts = config["SKIP_EXT"].split(",")
    else:
        skip_exts = [config["SKIP_EXT"]]

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

    ownerman = await bot.fetch_user(bot.owner_id)

    if config["OWNER_DM_RESTART"]:
        await ownerman.send(
            "Started/restarted at: `" + str(datetime.datetime.now()) + "`"
        )

    await ownerman.send(
        f"We have a total of {str(len(bot.slash_commands))} slash commands"
    )
    await ownerman.send(
        f"We have a total of {str(len(bot.application_commands))} app commands"
    )

    if load_error:
        t = error
        if len(error) > 1000:
            t = await paste(error)
        await ownerman.send(t)
