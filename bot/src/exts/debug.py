from disnake.ext import commands

from .util_functions import *

@commands.slash_command(name="gitstatus")
async def git_status(self, ctx):
    """Show the output of git status"""
    commit_msg = await run_command_shell(
        "git --no-pager log --decorate=short --pretty=oneline -n1"
    )
    await ctx.response.send_message(embed=inf_msg("Git Status", "```" + commit_msg + "```"))

@commands.slash_command(name="purgesyslog")
async def purge_syslog(self, ctx):
    """Delete all existing syslogs (USE WITH CARE) (Owner only)"""
    if ctx.message.author.id == self.bot.owner_id:
        purged = await run_command_shell("rm system_log* -v")
        await ctx.response.send_message(
            embed=inf_msg("Syslog Purger", "We purged:\n```" + purged + "```")
        )
    else:
        await ctx.response.send_message(embed=err_msg("Oops", wrong_perms("purgesyslog")))

@disnake.ext.commands.is_owner()
@commands.slash_command(name="ds")
async def ds(self, ctx, *, what):
    """Debug shell for the bot owner"""
    what = what.replace("'", "'")
    out = await run_command_shell(f"/bin/bash -c '{what}'")
    msg = f"```{out}```"
    if len(msg) > 1023:
        link = await paste(out)
        msg = f"See output here: {link}"
    await ctx.response.send_message(msg)



def setup(bot):
    print("Loading Debug extension")
    bot.add_slash_command(git_status)
    bot.add_slash_command(purge_syslog)
    bot.add_slash_command(ds)
    print("Done")
