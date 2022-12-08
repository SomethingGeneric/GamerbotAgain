from discord.ext import commands

# I hate this file ngl


class ThatsFuckedUp(commands.Cog):
    """Stuff from jasio"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mc = message.content.lower()
        mchan = message.channel

        if message.author != self.bot.user:
            if "michal moment" in mc:
                await mchan.send("yeah......", reference=message)

    @commands.command()
    async def forgor(self, ctx):
        """🦀🦀🦀🦀🦀"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(
            "https://tenor.com/view/i-forgot-i-forgor-meme-memes-kinemaster-gif-22374063",
        )

    @commands.command()
    async def elb(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(
            "https://tenor.com/view/i-request-elaboration-white-vision-paul-bettany-wandavision-i-want-an-explanation-gif-22928362",
        )

    @commands.command()
    async def facepalm(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(
            "https://tenor.com/view/facepalm-anime-jfc-gif-19368854",
        )


async def setup(bot):
    await bot.add_cog(ThatsFuckedUp(bot))
