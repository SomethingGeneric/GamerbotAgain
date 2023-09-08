from disnake.ext import commands
from .util_functions import *
import binascii
import os, re

bp = f"{config['volpath']}/no_bash.txt"

dont = ["dd", "fallocate", "doas", "pkexec", "truncate"]


def reload_ignore():
    if os.path.exists(bp):
        ignore = []
        ids = []
        with open(bp) as f:
            ids = f.read().split("\n")
        for nid in ids:
            ignore.append(nid)


ignore = []
reload_ignore()


def write_ignore(uid):
    with open(bp, "a+") as f:
        f.write(str(uid) + "\n")
    reload_ignore()


def remove_ignore(uid):
    ignore.remove(uid)
    with open(bp, "w") as f:
        f.write("\n".join(ignore))
    reload_ignore()


class Shell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @disnake.ext.commands.is_owner()
    @commands.slash_command(name="add-nobash")
    async def add_nobash(self, inter, uid):
        """I hope this is easy to figure out"""
        write_ignore(uid)
        await inter.send("Done")

    @disnake.ext.commands.is_owner()
    @commands.slash_command(name="remove-nobash")
    async def remove_nobash(self, inter, uid):
        """I hope this is easy to figure out"""
        remove_ignore(uid)
        await inter.send("Done")

    @commands.slash_command(name="reset-bash")
    async def reset_bash(self, inter, confirm="n"):
        """Reset my bash access"""
        try:
            if confirm == "y":
                un = "user_" + str(inter.author.id)
                await inter.send("Resetting your user.")
                await run_command_shell(
                    f"ssh punchingbag 'userdel {un} && rm -rf /home/{un}'"
                )
                await inter.send("Done.")
            else:
                await inter.send(
                    "Just to confirm, you want to nuke your bash user. If so, re-run with `y`",
                )
        except Exception as e:
            await inter.send(f"Error: ```{str(e)}```")

    async def doshell(self, inter, cmd, shell="bash"):
        if inter.guild is not None:
            guild_id = inter.guild.id
            permitted_guilds = config.get("permitted_guilds", [])
            if guild_id not in permitted_guilds:
                await inter.send("This guild is not permitted to use shell commands.")
                return

        if " " in cmd:
            if cmd.split(" ")[0] in dont:
                await inter.send(f"Do not `{cmd.split(' ')[0]}`")
                return
        elif cmd in dont:
            await inter.send(f"Do not `{cmd}`")
            return

        if str(inter.author.id) in ignore:
            await inter.send("No more bash for you")
            return

        if ":(){ :|:& };:" in cmd or re.search(r"(.)\|\1&", cmd):
            await inter.send("No forkbombs")
            write_ignore(inter.author.id)
            return

        un = "user_" + str(inter.author.id)

        await run_command_shell("scp /bot/bin/has_user punchingbag:.")
        test_user = await run_command_shell(f"ssh punchingbag './has_user {un}'")

        if "n" in test_user:  # no user
            await run_command_shell("scp /bot/bin/mk_user punchingbag:.")
            await run_command_shell(f"ssh punchingbag './mk_user {un}'")

        temp_script_fn = "." + str(binascii.b2a_hex(os.urandom(15)).decode("utf-8"))

        with open(temp_script_fn, "w") as f:
            f.write(f"#!/usr/bin/env {shell}\n{cmd}")

        await run_command_shell(f"scp {temp_script_fn} {un}@punchingbag:.")

        await run_command_shell(f"ssh {un}@punchingbag 'chmod +x {temp_script_fn}'")

        output = await run_command_shell(f"ssh {un}@punchingbag './{temp_script_fn}'")

        await run_command_shell(f"ssh {un}@punchingbag 'rm {temp_script_fn}'")

        msg = ""

        if len(output) > (999 - len(cmd)):
            link = await paste(f"Command was: '{cmd}', output:\n{output}")
            msg = f"See output: {link}"
        else:
            if len(output) != 0:
                msg = f"Command `{cmd}`, output: \n```{output}```"
            else:
                msg = f"Command: `{cmd}`, but no output was returned"

        await inter.send(msg)

    @commands.slash_command()
    async def bash(self, inter, *, cmd: str):
        """Run a command"""
        try:
            await inter.response.defer()
            await self.doshell(inter, cmd)
        except Exception as ex:
            await inter.send(f"Error: ```{str(ex)}```")


    async def mbash(self, inter, message):
        """Run a command"""
        try:
            await inter.response.defer()
            await self.doshell(inter, message.content)
        except Exception as ex:
            await inter.send(f"Error: ```{str(ex)}```")


def setup(bot):
    print("Loading shell extension")
    bot.add_cog(Shell(bot))
