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

    ownerman = await bot.fetch_user(bot.owner_id)

    if config["owner_dm_restart"]:
        await ownerman.send(
            "Started/restarted at: `" + str(datetime.datetime.now()) + "`"
        )

    if load_error:
        t = error
        if len(error) > 1000:
            t = await paste(error)
        await ownerman.send(t)
    
    @bot.event
    async def on_message(message):
        pattern = r'(\d{1,2}:\d{2})\s([a-zA-Z/]+)'
        match = re.search(pattern, message.content)
        if match:
            time_str, tz_str = match.groups()
            dt = datetime.datetime.strptime(time_str, '%H:%M')
            tz = pytz.timezone(tz_str)
            dt = tz.localize(dt).astimezone(pytz.UTC)
            await message.channel.send(f"The time {time_str} {tz_str} is {dt.strftime('%H:%M')} UTC.")
        else:
            pattern = r'(\d{1,2}:\d{2})'
            match = re.search(pattern, message.content)
            if match:
                time_str = match.group(1)
                tz_str = user_timezones.get(message.author.id)
                if tz_str:
                    dt = datetime.datetime.strptime(time_str, '%H:%M')
                    tz = pytz.timezone(tz_str)
                    dt = tz.localize(dt).astimezone(pytz.UTC)
                    await message.channel.send(f"Your time {time_str} is {dt.strftime('%H:%M')} UTC.")
