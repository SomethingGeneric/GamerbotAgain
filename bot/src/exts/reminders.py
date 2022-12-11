from datetime import datetime
import os

from disnake.ext import commands, tasks
import dateutil.parser
import yaml

from .util_functions import *


class reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = f"{config['volpath']}/reminders.yaml"

        if os.path.exists(self.storage):
            with open(self.storage, "r") as stream:
                try:
                    self.data = yaml.safe_load(stream)
                except yaml.YAMLError as err:
                    print(err)
        else:
            self.data = []

        self.iterate_reminders.start()

    def cog_unload(self):
        self.iterate_reminders.cancel()

    def write_data(self):
        with open(self.storage, "w") as f:
            yaml.dump(self.data, f)

    @commands.slash_command()
    async def show_time(self, inter):
        """Get bot's local time for reminders"""
        try:
            await inter.send(f"It's currently `{str(datetime.now())}`")
        except Exception as e:
            await inter.send(f"Error: `{str(e)}`")

    @commands.slash_command()
    async def remind(self, inter, what: str, when: str):
        """Set a reminder"""
        try:
            dtobj = dateutil.parser.parse(
                when
            )  # can't save this in yaml, so this is just to catch invalid strings before they get saved
            reminder = {"user": inter.author.id, "text": what, "when": when}
            self.data.append(reminder)
            self.write_data()
            await inter.send(
                f"I've saved your reminder `{what}` for `{str(dtobj)}`."
            )  # maybe we *should* spit out the dateime obj here?
            # DM user?
        except Exception as e:
            await inter.send(f"Error while creating reminder: `{str(e)}`.")

    @commands.slash_command()
    async def show_reminders(self, inter):
        """List all of your reminders"""
        try:
            await inter.response.defer()
            if len(self.data) != 0:
                n = 0
                for reminder in self.data:
                    if inter.author.id == int(reminder["user"]):
                        await inter.send(
                            f"{str(n)}. `{reminder['text']}`, at {reminder['when']}."
                        )
                    n += 1  # btw this isn't an indent error. (the idea is that maybe we'll do an 'admin' cancel reminder type beat)
            else:
                await inter.send(
                    "There are no reminders at all, hence there are none for you."
                )
        except Exception as e:
            await inter.send(f"Error: `{str(e)}`")

    @commands.slash_command()
    async def cancel_reminder(self, inter, event_id=None):
        """Cancel one of your reminders"""

        if len(self.data) == 0:
            await inter.send("There are no reminders...?")
            return

        if event_id is None:
            await inter.send(
                "Use `/show_reminders` to get the ID of the one you'd like to cancel."
            )
        else:
            n = 0
            for reminder in self.data:
                if int(event_id) == n and int(reminder["user"]) == inter.author.id:
                    self.data.remove(reminder)
                    self.write_data()
                    await inter.send(f"Removed your reminder #{event_id}.")
                    return
                n += 1
            await inter.send(
                f"You've either used an invalid id, or it isn't a reminder *you* created."
            )

    # TODO: dump all (admin)? - doesn't seem necesary rn (just '/ds cat /gb-data/reminders.yaml')
    # TODO: cancel reminder (admin) (maybe?)
    # TODO: cancel reminder
    # TODO: localize reminder by user timezone (hrrrg)

    @tasks.loop(seconds=60)
    async def iterate_reminders(self):
        try:
            for reminder in self.data:
                dt = dateutil.parser.parse(reminder["when"])  # i fucking love python
                if datetime.now() > dt:  # i fucking love python (x2)
                    who = await self.bot.fetch_user(int(reminder["user"]))
                    await who.send(
                        who.mention,
                        embed=inf_msg(
                            "Reminder!",
                            f"Hey there! You asked me to remind you: `{reminder['text']}`",
                        ),
                    )
                    self.data.remove(reminder)
                    self.write_data()
        except Exception as e:
            print(f"Reminder task error: '{str(e)}'")

    @iterate_reminders.before_loop
    async def before_status_task(self):
        print("Waiting for bot to be ready before starting reminder task")
        await self.bot.wait_until_ready()
        print("Bot is ready. Enabling reminder task")


def setup(bot):
    bot.add_cog(reminders(bot))
