from disnake.ext import commands

# I hate this file ngl

# TODO: Fix this?
"""
@commands.Cog.listener()
async def on_message(self, message):
    mc = message.content.lower()
    mchan = message.channel

    if message.author != self.bot.user:
        if "michal moment" in mc:
            await mchan.send("yeah......", reference=message)
"""


@commands.slash_command()
async def forgor(self, inter):
    """🦀🦀🦀🦀🦀"""
    try:
        await inter.message.delete()
    except Exception as e:
        # This should only break if we don't have manage message perm
        pass
    await inter.send(
        "https://tenor.com/view/i-forgot-i-forgor-meme-memes-kinemaster-gif-22374063",
    )


@commands.slash_command()
async def elb(self, inter):
    try:
        await inter.message.delete()
    except Exception as e:
        # This should only break if we don't have manage message perm
        pass
    await inter.send(
        "https://tenor.com/view/i-request-elaboration-white-vision-paul-bettany-wandavision-i-want-an-explanation-gif-22928362",
    )


@commands.slash_command()
async def facepalm(self, inter):
    try:
        await inter.message.delete()
    except Exception as e:
        # This should only break if we don't have manage message perm
        pass
    await inter.send(
        "https://tenor.com/view/facepalm-anime-jfc-gif-19368854",
    )


def setup(bot):
    print("Loading ThatsFuckedUp")
    bot.add_slash_command(forgor)
    bot.add_slash_command(elb)
    bot.add_slash_command(facepalm)
    print("Done")
