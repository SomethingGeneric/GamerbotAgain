import json
import urllib
import urllib.parse

import duckduckgo
import gmplot
from discord.ext import commands

import random
from util_functions import *


# Fun internet things

# TODO: find correct exceptions for this
async def get_as_json(url):
    try:
        data = await run_command_shell('curl "' + url + '"')
        return json.loads(data)
    except Exception as e:
        return '{"haha":"heeho"}'


class Internet(commands.Cog):
    """Useful tools on the interwebs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kernel(self, ctx):
        """Get Linux kernel info for host and latest"""
        try:
            m = await ctx.send(embed=inf_msg("Kernel", "Getting kernel info."))
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
            await ctx.send(embed=inf_msg("Kernel", msg))
        except Exception as e:
            await ctx.send(
                embed=err_msg("Kernel", "Had an issue getting info: `" + str(e) + "`")
            )
            syslog.log("Internet-Important", "Kernel command had error: " + str(e))

    @commands.command()
    async def search(self, ctx, *, query):
        """Use if someone is making you do resarch for them"""
        url = "https://www.google.com/search?q="
        async with ctx.typing():
            await asyncio.sleep(1)
        await ctx.send(embed=inf_msg("Go to: ", url + urllib.parse.quote(query)))

    @commands.command()
    async def traceroute(self, ctx, *, url):
        """Run traceroute on a url"""
        try:
            if "." in url:
                url.replace(";", "").replace("&", "").replace("&&", "")
                if " " in url:
                    url = url.split(" ")[0]
                await ctx.send(
                    ctx.message.author.mention,
                    embed=warn_msg(
                        "Wait time for traceroute", "This will take a while. Working..."
                    ),
                )

                syslog.log("Internet", "Starting traceroute of " + url)

                out = await run_command_shell("traceroute " + url)
                if len(out) < 1024:
                    await ctx.send(
                        embed=inf_msg("Traceroute output", "```" + str(out) + "```")
                    )
                else:
                    link = await paste(out)
                    await ctx.send(
                        ctx.message.author.mention,
                        embed=inf_msg(
                            "Output",
                            "The traceroute output is too long, so here's a link: "
                            + link,
                        ),
                    )

                syslog.log("Internet", "Finished traceroute of " + url)
            else:
                await ctx.send(
                    ctx.message.author.mention,
                    embed=err_msg("You goofed", " that's not an address :|"),
                )
        except Exception as e:
            await ctx.send(embed=err_msg("Traceroute error", "`" + str(e) + "`"))
            syslog.log(
                "Internet-Imporant", "Had an issue running traceroute: `" + str(e) + "`"
            )

    @commands.command()
    async def whois(self, ctx, *, url):
        """Lookup data on a domain"""
        try:
            if "." in url:
                url.replace(";", "").replace("&", "").replace("&&", "")
                if " " in url:
                    url = url.split(" ")[0]
                await ctx.send(
                    ctx.message.author.mention,
                    embed=warn_msg(
                        "Wait time for whois", "This will take a while. Working..."
                    ),
                )
                syslog.log("Internet", "Querying WHOIS for " + url)
                out = await run_command_shell("whois " + url)
                if len(out) > 1024:
                    link = await paste(out)
                    await ctx.send(
                        ctx.message.author.mention,
                        embed=inf_msg(
                            "Output",
                            "The whois output is too long, so here's a link: " + link,
                        ),
                    )
                else:
                    await ctx.send(
                        embed=inf_msg("Whois output", "```" + str(out) + "```")
                    )
                syslog.log("Internet", "Done querying WHOIS for " + url)
            else:
                await ctx.send(
                    ctx.message.author.mention,
                    embed=err_msg("You goofed", " that's not an address :|"),
                )
        except Exception as e:
            await ctx.send(embed=err_msg("Whois error", "`" + str(e) + "`"))
            syslog.log(
                "Internet-Important", "Had an issue running whois: `" + str(e) + "`"
            )

    @commands.command()
    async def nmap(self, ctx, *, url):
        """Scan a url/ip for open ports"""
        try:
            if "." in url:
                url.replace(";", "").replace("&", "").replace("&&", "")
                if " " in url:
                    url = url.split(" ")[0]
                await ctx.send(
                    ctx.message.author.mention,
                    embed=warn_msg(
                        "Wait time for nmap", "This will take a while. Working..."
                    ),
                )
                syslog.log("Internet", "Querying NMAP for " + url)
                out = await run_command_shell("nmap -A -vv -Pn " + url)
                if len(out) > 1024:
                    link = await paste(out)
                    await ctx.send(
                        ctx.message.author.mention,
                        embed=inf_msg(
                            "Output",
                            "The nmap output is too long, so here's a link: " + link,
                        ),
                    )
                else:
                    await ctx.send(
                        embed=inf_msg("Nmap output", "```" + str(out) + "```")
                    )
                syslog.log("Internet", "Done querying NMAP for " + url)
            else:
                await ctx.send(
                    ctx.message.author.mention,
                    embed=err_msg("You goofed", " that's not an address :|"),
                )
        except Exception as e:
            await ctx.send(embed=err_msg("NMAP error", "`" + str(e) + "`"))
            syslog.log(
                "Internet-Important", "Had an issue running nmap: `" + str(e) + "`"
            )

    @commands.command()
    async def geoip(self, ctx, *, ip):
        """Get GeoIP of an address"""
        try:
            dat = get_geoip(ip)

            msg = "```"

            for key, value in dat.items():
                msg += key.replace("_", " ") + ": " + str(value) + "\n"

            msg += "```\n"

            if "latitude" in dat.keys() and "longitude" in dat.keys():
                msg += f"Google maps: http://www.google.com/maps/place/{dat['latitude']},{dat['longitude']}"

            await ctx.send(embed=inf_msg("GeoIP for `" + ip + "`", msg))
            syslog.log("Internet", "Queried GeoIP for " + ip)

        except Exception as e:
            await ctx.send(
                embed=err_msg(
                    "GeoIP error", "Had an issue getting GeoIP data: `" + str(e) + "`"
                )
            )
            syslog.log(
                "Internet-Important",
                "Had an issue getting GeoIP data: `" + str(e) + "`",
            )

    """
    @commands.command(aliases=["tr-map"])
    async def trmap(self, ctx, *, ip):
        try:

            cmd = "traceroute -n 8.8.8.8 | tail -n+2 | awk '{ print $2 }'".replace(
                "8.8.8.8", ip
            )

            await ctx.send(
                embed=warn_msg(
                    "Trace-map",
                    "Running traceroute for `" + ip + "`\n This will take a while.",
                )
            )

            out = await run_command_shell(cmd)

            addrs = out.split("\n")

            cleanup = []

            sum_hops = ""

            for line in addrs:
                if not "*" in line:
                    if line != "10.0.0.1" and line != "192.168.1.1":
                        cleanup.append(line)
                        sum_hops += "- " + line + "\n"

            await ctx.send(embed=inf_msg("Trace-map", "Hops:\n```" + sum_hops + "```"))

            lat_list = []
            long_list = []

            for line in cleanup:
                print("Getting data for: " + line)
                dat = get_geoip(line)
                if "message" in dat.keys():
                    await ctx.send(
                        embed=err_msg(
                            "Trace-map", "No location data for `" + line + "`"
                        )
                    )
                else:
                    lat_list.append(float(dat["latitude"]))
                    long_list.append(float(dat["longitude"]))

            gmap3 = gmplot.GoogleMapPlotter(
                0.0, 0.0, 0, apikey=os.getenv(("MAPS_KEY")
            )

            # Points gang
            gmap3.scatter(lat_list, long_list, "#FF0000", marker=False)

            # Lines gang
            gmap3.plot(lat_list, long_list, "cornflowerblue", edge_width=2.5)

            idh = (
                "".join(random.choices(string.ascii_uppercase + string.digits, k=25))
                + ".html"
            )

            fn = os.getenv(("PASTE_BASE") + idh

            # Save time
            gmap3.draw(fn)

            await ctx.send(
                ctx.message.author.mention,
                embed=inf_msg(
                    "GeoIP",
                    "Map is available at: " + os.getenv(("PASTE_URL_BASE") + idh,
                ),
            )

        except Exception as e:
            await ctx.send(
                ctx.message.author.mention,
                embed=err_msg(
                    "GeoIP", "Had an issue making your map: `" + str(e) + "`"
                ),
            )
            syslog.log(
                "Internet-Important", "Had an issue making trmap: `" + str(e) + "`"
            )
    """

    @commands.command()
    async def ddg(self, ctx, *, query):
        await ctx.send(duckduckgo.get_zci(query), reference=ctx.message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "hey gamerbot" in message.content:
            await message.channel.send(
                duckduckgo.get_zci(message.content.replace("hey gamerbot", "")),
                reference=message,
            )


# End fun internet things
async def setup(bot):
    await bot.add_cog(Internet(bot))
