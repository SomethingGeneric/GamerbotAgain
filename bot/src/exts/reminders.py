from datetime import datetime
import os

from disnake.ext import commands, tasks
import dateutil.parser
import yaml
import pytz
from pytz import timezone, all_timezones
from dateutil import parser


from .util_functions import *


class reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.storage = f"{config['volpath']}/reminders.yaml"

        self.urtz = f"{config['volpath']}/user-tzobj.yamlf"

        if os.path.exists(self.storage):
            with open(self.storage, "r") as stream:
                try:
                    self.data = yaml.safe_load(stream)
                except yaml.YAMLError as err:
                    print(err)
        else:
            self.data = []

        if os.path.exists(self.urtz):
            with open(self.urtz, "r") as stream:
                try:
                    self.tzdata = yaml.safe_load(stream)
                except yaml.YAMLError as err:
                    print(err)
        else:
            self.tzdata = {}

        self.iterate_reminders.start()

    def cog_unload(self):
        self.iterate_reminders.cancel()
        self.write_data()

    def write_data(self):
        with open(self.storage, "w") as f:
            yaml.dump(self.data, f)

        with open(self.urtz, "w") as f:
            yaml.dump(self.tzdata, f)

    @commands.slash_command()
    async def show_time(self, inter):
        """Get bot's local time for reminders"""
        try:
            await inter.response.defer()
            utc_ref = datetime.utcnow()
            msg = f"It's currently `{str(utc_ref)}` for me."
            if inter.author.id in self.tzdata.keys():
                their_timezone_obj = timezone(self.tzdata[inter.author.id])
                for_them = their_timezone_obj.fromutc(utc_ref)
                msg += f"\nAnd, it's `{str(for_them)}` for you."
            await inter.send(msg)
        except Exception as e:
            await inter.send(f"Error: `{str(e)}`")

    @commands.slash_command()
    async def time_for(self, inter, user: disnake.User):
        """Wondering what time it is for a friend?"""
        try:
            await inter.response.defer()
            if user.id in self.tzdata.keys():
                utc_ref = datetime.utcnow()
                their_timezone_obj = timezone(self.tzdata[user.id])
                for_them = their_timezone_obj.fromutc(utc_ref)
                await inter.send(f"It's `{for_them}` for {user.mention}.")
            else:
                await inter.send(f"{user.mention} hasn't used `/mytz` :(")
        except Exception as e:
            await inter.send(f"Whoops! Error: `{str(e)}`")

    @commands.slash_command()
    async def mytz(self, inter, timez: str):
        """Tell me your timezone!"""
        try:
            await inter.response.defer()
            if (
                timez in pytz.all_timezones or timez.upper() in pytz.all_timezones
            ):  # woo yea
                self.tzdata[inter.author.id] = timez
                await inter.send("Noted!")
            else:
                await inter.send("That doesn't seem to be a timezone.")
        except Exception as e:
            await inter.send("Error: ```" + str(e) + "```")

    @commands.slash_command()
    async def remind(self, inter, what: str, when: str, utc: bool):
        """Set a reminder"""
        try:
            if not utc and inter.author.id not in self.tzdata.keys():
                await inter.send(
                    "To set a non-utc reminder, you'll need to use `/mytz` first."
                )
                return

            dtobj = dateutil.parser.parse(
                when
            )  # can't save this in yaml, so this is just to catch invalid strings before they get saved
            reminder = {"user": inter.author.id, "text": what, "when": when, "utc": utc}
            self.data.append(reminder)
            self.write_data()

            msg = f"I've saved your reminder `{what}` for `{str(dtobj)}`"

            if utc:
                msg += " UTC."
            else:
                msg += " local time."

            await inter.send(msg)  # maybe we *should* spit out the dateime obj here?
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
    async def cancel_reminder(self, inter, event_id: int):
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

    @tasks.loop(seconds=60)
    async def iterate_reminders(self):
        try:
            for reminder in self.data:
                dt_raw = dateutil.parser.parse(
                    reminder["when"]
                )  # i fucking love python
                utc_ref = datetime.utcnow()

                if reminder["utc"]:
                    if utc_ref > dt_raw:
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
                else:
                    their_tz = timezone(
                        self.tzdata[int(reminder["user"])]
                    )  # good luck with this one, Satan
                    rem_time = their_tz.localize(
                        dateutil.parser.parse(reminder["when"])
                    )
                    comp_local_time = their_tz.localize(utc_ref)
                    if comp_local_time > rem_time:
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
            owner = await self.bot.fetch_user(self.bot.owner_id)
            await owner.send(f"Reminder task error: '{str(e)}'")

    @iterate_reminders.before_loop
    async def before_status_task(self):
        print("Waiting for bot to be ready before starting reminder task")
        await self.bot.wait_until_ready()
        print("Bot is ready. Enabling reminder task")


def setup(bot):
    bot.add_cog(reminders(bot))
