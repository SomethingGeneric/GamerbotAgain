from disnake.ext import commands

from .util_functions import *


@commands.slash_command()
async def source(ctx):
    """Bot source code link"""
    await ctx.response.send_message(
        "My source code lives here: https://github.com/SomethingGeneric/Gamerbot"
    )


@commands.slash_command()
async def license(ctx):
    """Bot license file"""
    await ctx.response.send_message(
        "My license lives here: https://github.com/SomethingGeneric/Gamerbot/-/blob/main/LICENSE",
    )


@commands.slash_command()
async def report(ctx):
    """Report bot issues"""
    await ctx.response.send_message(
        "You can file issues here: https://github.com/SomethingGeneric/Gamerbot/issues",
    )


@commands.slash_command()
async def version(ctx):
    """Get git info"""
    commit_msg = await run_command_shell(
        "git --no-pager log --decorate=short --pretty=oneline -n1"
    )
    msg = ""
    msg += "Latest Git commit: \n"
    msg += "```" + commit_msg + "```"
    await ctx.response.send_message(f"{msg}")


@commands.slash_command()
async def invite(ctx):
    """Add me to another server"""
    await ctx.response.send_message(
        "https://discord.com/api/oauth2/authorize?client_id=763559371628085288&permissions=1629910589175&scope=bot%20applications.commands",
    )


@commands.slash_command()
async def support(ctx):
    """Get support for Gamerbot"""
    await ctx.response.send_message(
        "Join our server. :)", "https://discord.gg/j4nAea7cAs"
    )


def setup(bot):
    print("Loading About ext.")
    bot.add_slash_command(source)
    bot.add_slash_command(license)
    bot.add_slash_command(report)
    bot.add_slash_command(version)
    bot.add_slash_command(invite)
    bot.add_slash_command(support)
    print("Done.")
