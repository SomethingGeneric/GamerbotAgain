from disnake.ext import commands
import json, os, requests, asyncio, random, toml

from .util_functions import config

volpath = config["volpath"]

primary_url = "https://xkcd.com/info.0.json"
comic_url = "https://xkcd.com/CN/info.0.json"

data_fn = f"{volpath}/xkcd.toml"


class xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = None
        self.data_done = False

    async def setup_data(self):
        try:
            self.data_done = False
            if self.bot.owner_id is None:
                print("Owner ID not available, skipping DM notifications for XKCD setup")
                owner = None
            else:
                owner = await self.bot.fetch_user(self.bot.owner_id)
                await owner.send("Starting XKCD data work")
            if not os.path.exists(data_fn):
                if owner:
                    await owner.send(
                        "Doing full data download for XKCD. This will take a while"
                    )
                self.data = {}
                latest_comic = int(requests.get(primary_url).json()["num"])
                for i in range(1, latest_comic + 1):
                    try:
                        print(f"Getting data for comic {str(i)}")
                        self.data[i] = requests.get(
                            comic_url.replace("CN", str(i))
                        ).json()
                        await asyncio.sleep(random.uniform(0.1, 0.5))
                    except Exception as e:
                        print(f"Error getting comic {str(i)}: {str(e)}")
                        if owner:
                            await owner.send(f"Error getting comic {str(i)}: {str(e)}")
                with open(data_fn, "w") as f:
                    toml.dump(self.data, f)
                if owner:
                    await owner.send("Done with XKCD initial download")
            else:
                # await owner.send("Loading XKCD data from file")
                self.data = toml.load(data_fn)

                latest_comic = int(requests.get(primary_url).json()["num"])
                if self.data is not None and latest_comic not in self.data.keys():
                    highest_saved = 0
                    for key, _ in self.data.items():
                        if key > highest_saved:
                            highest_saved = key
                    for i in range(highest_saved, latest_comic + 1):
                        try:
                            print(f"Getting data for comic {str(i)}")
                            self.data[i] = requests.get(
                                comic_url.replace("CN", str(i))
                            ).json()
                            await asyncio.sleep(random.uniform(0.1, 0.5))
                        except Exception as e:
                            print(f"Error getting comic {str(i)}: {str(e)}")
                            if owner:
                                await owner.send(f"Error getting comic {str(i)}: {str(e)}")
                    with open(data_fn, "w") as f:
                        toml.dump(self.data, f)
                # await owner.send("All done with XKCD loading")
            self.data_done = True
            if owner:
                await owner.send("I have unlocked XKCD command for usage.")
        except Exception as e:
            print("XKCD setup error: " + str(e))

    def cog_uload(self):
        print("Saving XKCD data")
        with open(data_fn, "w") as f:
            toml.dump(self.data, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Getting or loading XKCD data")
        await self.setup_data()

    @commands.slash_command()
    async def reset_xkcd(self, inter):
        """Reset saved XKCD data (owner ownly)"""
        if inter.author.id == self.bot.owner_id:
            try:
                os.remove(data_fn)
                await inter.send("Deleted data. Restarting load.")
                await self.setup_data()
                await inter.send("Reset done")
            except Exception as e:
                await inter.send("Problem: `" + str(e) + "`")
        else:
            await inter.send("nope")

    @commands.slash_command()
    async def xkcdsearch(self, inter, *, query: str):
        """Search for XKCD by title or alt-text"""
        try:
            if not self.data_done:
                await inter.send("Data is not yet loaded. Try again later!")
                return
            await inter.response.defer()
            for k, v in self.data.items():
                if (
                    query.lower() in v["safe_title"].lower()
                    or query.lower() in v["alt"].lower()
                ):
                    await inter.send(
                        f"You're probably looking for: https://xkcd.com/{str(k)}"
                    )
                    return
            await inter.send(f"Not found: `{query}`")
        except Exception as e:
            await inter.send(f"XKCD Error: `{str(e)}`")


def setup(bot):
    print("Loading XKCD ext")
    bot.add_cog(xkcd(bot))
