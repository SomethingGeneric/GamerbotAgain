import asyncio
import disnake
import geoip2.database
import aiohttp
import os, sys
import threading
import binascii
import toml
import re

if not os.path.exists("config.toml"):
    print("No config found")
    sys.exit(1)

config = toml.load("config.toml")


def fancy_msg(title, text, color, footnote=None):
    e = disnake.Embed(colour=color)
    e.add_field(name=title, value=text, inline=False)

    if footnote is not None:
        e.set_footer(text=footnote)

    return e


def err_msg(title, text, footnote=None):
    return fancy_msg(title, text, disnake.Colour.red(), footnote)


def warn_msg(title, text, footnote=None):
    return fancy_msg(title, text, disnake.Colour.gold(), footnote)


def inf_msg(title, text, footnote=None):
    return fancy_msg(title, text, disnake.Colour.blurple(), footnote)


def image_embed(title, msg_type, dat):
    # see docs at
    # https://discordpy.readthedocs.io/en/stable/faq.html?highlight=embed#how-do-i-use-a-local-image-file-for-an-embed-image
    e = disnake.Embed(color=disnake.Colour.blurple())
    e.add_field(name="foo", value=title, inline=False)
    if msg_type == "rem":
        e.set_image(url=dat)
    else:
        e.set_image(url="attachment://" + dat)
    return e


# Simple file wrappers
def check(fn):
    if os.path.exists(fn):
        return True
    else:
        return False


def save(fn, text):
    with open(fn, "a+") as f:
        f.write(text + "\n")


def get(fn):
    if check(fn):
        with open(fn) as f:
            return f.read()


def ensure(fn):
    if not check(fn):
        os.makedirs(fn, exist_ok=True)


def get_stamp():
    os.system("date >> stamp")
    with open("stamp") as f:
        s = f.read()
    os.remove("stamp")
    return s


def is_whitelisted(word):
    if word in WHITELIST:
        return True
    else:
        return False


def wrong_perms(command):
    print("Someone just failed to run: '" + command + "'")
    return wrong_perms.replace("{command}", command)


# Maybe add: https://docs.python.org/3/library/shlex.html#shlex.quote ?
async def run_command_shell(command, grc=False):
    """Run command in subprocess (shell)."""

    kill = lambda proc: proc.kill()
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Status
    print("Started:", command, "(pid = " + str(process.pid) + ")", flush=True)

    kill_timer = threading.Timer(60, kill, [process])

    try:
        # Wait for the subprocess to finish
        kill_timer.start()
        stdout, stderr = await process.communicate()
    except:
        kill_timer.cancel()

    # Progress
    if process.returncode == 0:
        print("Done:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stdout.decode().strip()
    else:
        print("Failed:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stderr.decode().strip()

    kill_timer.cancel()

    if not grc:
        # Return stdout
        return result.strip().rstrip()
    else:
        return process.returncode, result.strip().rstrip()


async def isup(host):
    code, _ = await run_command_shell("ping -c 1 " + host)
    if code == 0:
        return True
    else:
        return False


async def paste(text):
    paste_fn = "." + str(binascii.b2a_hex(os.urandom(15)).decode("utf-8"))
    with open(paste_fn, "w") as f:
        f.write(text)
    link = await run_command_shell(f"cat {paste_fn} | nc termbin.com 9999")
    os.remove(paste_fn)
    return link.strip()


async def pastef(fn):
    link = await run_command_shell(f"cat {fn} | nc termbin.com 9999")
    return link.strip()


def get_geoip(ip):
    with geoip2.database.Reader("GeoLite2-City.mmdb") as reader:
        try:
            response = reader.city(ip)
            return {
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
        except Exception as e:
            return {"message": str(e)}


def split_string(text, max_length=130):
    # Split text into sentences using regular expression
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

    result = []
    current_part = ""

    for sentence in sentences:
        # Check if adding the current sentence exceeds the max length
        if len(current_part) + len(sentence) <= max_length:
            current_part += sentence + " "
        else:
            result.append(current_part.strip())
            current_part = sentence + " "

    # Add the last part
    result.append(current_part.strip())

    return result

async def webhook_log(message):
    webhook_url = "https://discord.com/api/webhooks/1290969368905126000/DhEzedmrOwHLOojj50PL_e0eVMJehUvHNRwHVFUgZP-QpB1HaXEbWvcZ67olSVOiaIM8"
    data = {
        "content": message
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=data) as response:
            if response.status == 200:
                print("Message posted successfully")
            else:
                print("Failed to post message")
