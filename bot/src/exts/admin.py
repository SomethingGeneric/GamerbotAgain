import disnake.ext.commands
from disnake.ext import commands


@disnake.ext.commands.is_owner()
@commands.slash_command(
    name="bot-info",
    description="Get info about the bot",
)
async def bot_info(inter):
    embed = disnake.Embed(
        title="Bot Info",
        colour=disnake.Colour.blurple(),
    )

    embed.add_field(name="Name", value=inter.bot.user, inline=True)
    embed.add_field(name="ID", value=inter.bot.user.id, inline=True)
    embed.add_field(name="Created At", value=inter.bot.user.created_at, inline=False)
    embed.add_field(name="Guilds", value=len(inter.bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(inter.bot.users), inline=True)

    embed.set_thumbnail(url=inter.bot.user.display_avatar.url)

    await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    print("Loading Admin Ext.")
    bot.add_slash_command(bot_info)
    print("Admin Ext. Loaded")
