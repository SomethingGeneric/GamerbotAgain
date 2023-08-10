from pyfiglet import Figlet

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="figlet")
    async def figlet(self, inter, *, text):
        """Generate ASCII art from text using pyfiglet"""
        f = Figlet()
        ascii_art = f.renderText(text)
        await inter.send(f"```\n{ascii_art}\n```")