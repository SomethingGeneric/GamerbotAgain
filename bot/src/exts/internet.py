import json
import urllib
import urllib.parse

import duckduckgo
import gmplot
from disnake.ext import commands

import random
from .util_functions import *


# Fun internet things

# TODO: find correct exceptions for this
async def get_as_json(url):
    try:
        data = await run_command_shell('curl "' + url + '"')
        return json.loads(data)
    except Exception as e:
        return '{"haha":"heeho"}'

@commands.slash_command()
async def kernel(ctx):
    """Get Linux kernel info for host and latest"""
    try:
        m = await ctx.response.send_message(embed=inf_msg("Kernel", "Getting kernel info."))
        data = await get_as_json("https://www.kernel.org/releases.json")
        new_ver = data["latest_stable"]["version"]
        mine = await run_command_shell("uname -r")
        msg = (
            "I'm running: `"
            + mine
            + "`\nKernel.org reports stable is: `"
            + new_ver
            + "`"
        )
        await m.delete()
        await ctx.response.send_message(embed=inf_msg("Kernel", msg))
    except Exception as e:
        await ctx.response.send_message(
            embed=err_msg("Kernel", "Had an issue getting info: `" + str(e) + "`")
        )

@commands.slash_command()
async def search(ctx, *, query):
    """Use if someone is making you do resarch for them"""
    url = "https://www.google.com/search?q="
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.response.send_message(embed=inf_msg("Go to: ", url + urllib.parse.quote(query)))

@commands.slash_command()
async def traceroute(ctx, *, url):
    """Run traceroute on a url"""
    try:
        if "." in url:
            url.replace(";", "").replace("&", "").replace("&&", "")
            if " " in url:
                url = url.split(" ")[0]
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=warn_msg(
                    "Wait time for traceroute", "This will take a while. Working..."
                ),
            )

            out = await run_command_shell("traceroute " + url)
            if len(out) < 1024:
                await ctx.response.send_message(
                    embed=inf_msg("Traceroute output", "```" + str(out) + "```")
                )
            else:
                link = await paste(out)
                await ctx.response.send_message(
                    ctx.message.author.mention,
                    embed=inf_msg(
                        "Output",
                        "The traceroute output is too long, so here's a link: "
                        + link,
                    ),
                )

        else:
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=err_msg("You goofed", " that's not an address :|"),
            )
    except Exception as e:
        await ctx.response.send_message(embed=err_msg("Traceroute error", "`" + str(e) + "`"))

@commands.slash_command()
async def whois(ctx, *, url):
    """Lookup data on a domain"""
    try:
        if "." in url:
            url.replace(";", "").replace("&", "").replace("&&", "")
            if " " in url:
                url = url.split(" ")[0]
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=warn_msg(
                    "Wait time for whois", "This will take a while. Working..."
                ),
            )
            out = await run_command_shell("whois " + url)
            if len(out) > 1024:
                link = await paste(out)
                await ctx.response.send_message(
                    ctx.message.author.mention,
                    embed=inf_msg(
                        "Output",
                        "The whois output is too long, so here's a link: " + link,
                    ),
                )
            else:
                await ctx.response.send_message(
                    embed=inf_msg("Whois output", "```" + str(out) + "```")
                )
        else:
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=err_msg("You goofed", " that's not an address :|"),
            )
    except Exception as e:
        await ctx.response.send_message(embed=err_msg("Whois error", "`" + str(e) + "`"))

@commands.slash_command()
async def nmap(ctx, *, url):
    """Scan a url/ip for open ports"""
    try:
        if "." in url:
            url.replace(";", "").replace("&", "").replace("&&", "")
            if " " in url:
                url = url.split(" ")[0]
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=warn_msg(
                    "Wait time for nmap", "This will take a while. Working..."
                ),
            )
            out = await run_command_shell("nmap -A -vv -Pn " + url)
            if len(out) > 1024:
                link = await paste(out)
                await ctx.response.send_message(
                    ctx.message.author.mention,
                    embed=inf_msg(
                        "Output",
                        "The nmap output is too long, so here's a link: " + link,
                    ),
                )
            else:
                await ctx.response.send_message(
                    embed=inf_msg("Nmap output", "```" + str(out) + "```")
                )
        else:
            await ctx.response.send_message(
                ctx.message.author.mention,
                embed=err_msg("You goofed", " that's not an address :|"),
            )
    except Exception as e:
        await ctx.response.send_message(embed=err_msg("NMAP error", "`" + str(e) + "`"))

@commands.slash_command()
async def geoip(ctx, *, ip):
    """Get GeoIP of an address"""
    try:
        dat = get_geoip(ip)

        msg = "```"

        for key, value in dat.items():
            msg += key.replace("_", " ") + ": " + str(value) + "\n"

        msg += "```\n"

        if "latitude" in dat.keys() and "longitude" in dat.keys():
            msg += f"Google maps: http://www.google.com/maps/place/{dat['latitude']},{dat['longitude']}"

        await ctx.response.send_message(embed=inf_msg("GeoIP for `" + ip + "`", msg))

    except Exception as e:
        await ctx.response.send_message(
            embed=err_msg(
                "GeoIP error", "Had an issue getting GeoIP data: `" + str(e) + "`"
            )
        )

@commands.slash_command()
async def ddg(ctx, *, query):
    """Search DuckDuckGo"""
    await ctx.response.send_message(duckduckgo.get_zci(query), reference=ctx.message)

# TODO: Figure out listeners and fix
"""
@commands.Cog.listener()
async def on_message(self, message):
    if "hey gamerbot" in message.content:
        await message.channel.send(
            duckduckgo.get_zci(message.content.replace("hey gamerbot", "")),
            reference=message,
        )
"""

def setup(bot):
    print("Loading internet ext")
    bot.add_slash_command(kernel)
    bot.add_slash_command(search)
    bot.add_slash_command(traceroute)
    bot.add_slash_command(geoip)
    bot.add_slash_command(whois)
    bot.add_slash_command(ddg)
    bot.add_slash_command(nmap)
    print("Done")
