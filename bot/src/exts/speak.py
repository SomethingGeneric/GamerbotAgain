# Pip
from disnake.ext import commands, tasks

# Mine
from .channel_state import VoiceState
from .util_functions import *


class Speak(commands.Cog):
    """Text to speech go brr"""

    def __init__(self, bot):
        self.vs = VoiceState()

        self.bot = bot
        self.voice_client = None
        self.audiosrc = None
        self.isDone = False

        self.chat_channels = []

        if os.path.exists(".chatchannels"):
            with open(".chatchannels") as f:
                channels = f.read().strip().split("\n")
            for chan in channels:
                self.chat_channels.append(int(chan))

        print("Instance created and setup")

    def set_done(self):
        self.isDone = True

    async def speak_in_channel(
        self, inter, text="", chan=None, stealth=False, file=None
    ):
        if self.voice_client is None and not self.vs.check_state():
            print(
                "This cog was not playing, nor were others. It's go time.",
            )

            try:

                if inter is not None and inter.author.voice is not None:
                    channel = inter.author.voice.channel
                else:
                    channel = chan

                if channel is not None:
                    print(
                        "The author is in a channel, so we're attempting to join them.",
                    )
                    if file is None:
                        await run_command_shell(
                            'espeak-ng -w espeak.wav "' + text + '"'
                        )
                        print(
                            "We have the TTS audio file ready. Playing it.",
                        )
                    else:
                        print("We're using a file")
                    self.voice_client = await channel.connect()
                    self.vs.set_state("1")
                    print("We're in voice now.")
                    fn = "espeak.wav"
                    if file is not None:
                        fn = file
                    self.audiosrc = disnake.FFmpegPCMAudio(fn)
                    self.isDone = False
                    self.voice_client.play(
                        self.audiosrc,
                        after=lambda e: print("Player error: %s" % e)
                        if e
                        else self.set_done(),
                    )
                    while self.voice_client.is_playing():
                        self.isDone = False
                        if self.isDone:
                            break
                        await asyncio.sleep(1)
                    print("We're done playing. Cleaning up.")

                    await self.voice_client.disconnect()
                    self.voice_client = None
                    self.audiosrc = None
                    self.isDone = True
                    await run_command_shell("rm espeak.wav")
                    self.vs.set_state("0")
                    print("We're done cleaning up. All done!")
                    if stealth:
                        return True
                else:
                    if not stealth:
                        await inter.send(
                            embed=err_msg(
                                "Spoken Word", "You're not in a voice channel."
                            )
                        )
                    else:
                        return False
            except Exception as e:
                print("Error: " + str(e))
                await inter.send(embed=err_msg("Spoken Word", "`" + str(e) + "`"))

        else:
            await inter.send(
                embed=err_msg(
                    "Spoken Word", "I'm already in a voice channel, and busy."
                ),
                reference=inter.message,
            )
            print("VC is busy somewhere. Doing nothing.")

    @commands.slash_command()
    async def tts(self, inter, *, thing, stealth=False):
        """Talk in voice channel"""
        await inter.response.defer()
        print("Calling speakInChannel for " + inter.author.display_name)
        await self.speak_in_channel(
            inter, inter.author.display_name + " says " + thing, None, False
        )
        await inter.send("Done!")

    async def do_meow(self, inter=None, chan=None):
        files = os.listdir("sounds")
        fn = "sounds/" + random.choice(files)
        print("Playing: " + fn)
        await self.speak_in_channel(inter=inter, chan=chan, file=fn)

    @commands.slash_command()
    async def meow(self, inter):
        """I am a cat :)"""
        await inter.response.defer()
        await self.do_meow(inter)
        await inter.send("Meow")

    @commands.Cog.listener()
    async def on_message(self, message):
        if " bee " in message.content.lower() or " bees " in message.content.lower():
            print("BEE MOVIE ALERT!!")
            with open("data/bee.txt") as f:
                quote = random.choice(f.read().split("\n"))
                if message.author.voice is not None:
                    inter = await self.bot.get_context(message)
                    print("Speak-Client", "Initializing meme session")
                    tried = await self.speak_in_channel(inter, quote, None, True)
                    if tried:
                        print("SPOKE BEE MOVIE QUOTE IN VOICE CHANNEL!!")
                    else:
                        print(
                            "Falling back to text since voice is too busy for memes.",
                        )
                        await message.channel.send("`" + quote + "`")
                        print("SENT BEE MOVIE QUOTE IN TEXT CHAT")
                else:
                    print(
                        "Falling back to text since voice is too busy for memes. (Voice not attempted)",
                    )
                    await message.channel.send("`" + quote + "`")
                    print("SENT BEE MOVIE QUOTE IN TEXT CHAT")

        if (
            message.channel.id in self.chat_channels
            and message.author != self.bot.user
            and message.content != "-makechatchannel"
            or "hey chatterbot" in message.content
        ):
            resp = await run_command_shell(
                'python3 bin/thechatbot.py "'
                + message.content.replace('"', "'").replace("hey chatterbot", "")
                + '"'
            )

            if len(resp) < 400:
                await message.channel.send(resp, reference=message)
            else:
                url = await paste(resp)
                await message.channel.send(url, reference=message)
            if message.author.voice is not None:
                inter = await self.bot.get_context(message)
                print("Speaking response as well")
                await self.speak_in_channel(inter=inter, text=resp)


def setup(bot):
    print("Loading speak ext")
    bot.add_cog(Speak(bot))
