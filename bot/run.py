#!/usr/bin/env python3

from src.main import bot, config

if __name__ == "__main__":
    print("Starting bot")
    bot.run(config["token"])
