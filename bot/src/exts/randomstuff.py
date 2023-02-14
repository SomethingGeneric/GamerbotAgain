import disnake
from disnake.ext import commands

from .util_functions import *


class RandomThings(commands.Cog):
    """Randomness"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter):
        """pong."""
        await inter.send(
            "pong. :upside_down: :gun:", file=disnake.File("images/pong.jpg")
        )

    @commands.slash_command()
    async def gcache(self, inter, *, url):
        """For legal reasons this isn't real"""
        await inter.send(
            f"https://www.google.com/search?q=cache:{url.replace('https://','').replace('http://','')}"
        )

    @commands.slash_command()
    async def math(self, inter, *, exp):
        """Do simple math on an expression (uses BC)"""
        res = await run_command_shell('echo "' + exp + '" | bc')
        if len(res) != 0:
            if len(res) < 1998:
                await inter.send(embed=inf_msg("Eval", "`" + str(res) + "`"))
            else:
                url = await paste(res)
                await inter.send(
                    embed=inf_msg(
                        "Eval", "Output was too many characters. Here's a link: " + url
                    )
                )
        else:
            await inter.send(embed=warn_msg("Eval", "No output."))


def setup(bot):
    print("Adding random ext")
    bot.add_cog(RandomThings(bot))
