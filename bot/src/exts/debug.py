from disnake.ext import commands

from .util_functions import *


class DebugStuff(commands.Cog):
    """This should be self-explanatory"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def check_cog(self, inter, name):
        """Check if cog is loaded"""
        if self.bot.get_cog(name) is not None:
            await inter.send(f"I was able to find `{name}`")
        else:
            await inter.send(f"I could not find `{name}`")

    @disnake.ext.commands.is_owner()
    @commands.slash_command()
    async def remove_cog(self, inter, name):
        """Force unload a cog"""
        if self.bot.remove_cog(name) is not None:
            await inter.send(f"I've removed `{name}`.")
        else:
            await inter.send(f"I could not remove `{name}`.")

    @disnake.ext.commands.is_owner()
    @commands.slash_command()
    async def add_cog(self, inter, name):
        """Force load a cog"""
        try:
            await inter.response.defer()  # cog loading *could* be slow
            self.bot.load_extension(name)
            await inter.send(f"I've loaded `{name}`.")
        except Exception as e:
            await inter.send(f"Failed to load `{name}`.")

    @disnake.ext.commands.is_owner()
    @commands.slash_command(name="ds")
    async def ds(self, inter, *, what):
        """Debug shell for the bot owner"""
        await inter.response.defer()
        what = what.replace("'", "'")
        out = await run_command_shell(f"/bin/bash -c '{what}'")
        msg = f"```{out}```"
        if len(msg) > 1023:
            link = await paste(out)
            msg = f"See output here: {link}"
        await inter.send(msg)


def setup(bot):
    print("Loading Debug extension")
    bot.add_cog(DebugStuff(bot))
