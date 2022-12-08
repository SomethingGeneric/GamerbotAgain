import disnake
import yaml, datetime
from disnake.ext import commands

with open("conf.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

intents = disnake.Intents().default()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.members = True

bot = commands.InteractionBot(
    status=disnake.Status.online,
    intents=intents,
)

# bot.load_extension('src.exts.moderation')
bot.load_extension("src.exts.admin")
bot.load_extension("src.exts.about")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} guilds, serving {len(bot.users)} users")

    if config["OWNER_DM_RESTART"]:
        ownerman = await bot.fetch_user(bot.owner_id)
        await ownerman.send(
            "Started/restarted at: `" + str(datetime.datetime.now()) + "`"
        )
