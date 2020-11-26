from datetime import datetime
from discord.ext import commands
from tools.logger import initialize_logging
from utils.config import GLOBAL as cfg
import asyncio
import logging
import os, sys

from tools.GoldDatabaseHandler import GoldDatabaseHandler

TOKEN = os.environ.get('DISCORD_TOKEN')

class PotatoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cfg['COMMANDS_PREFIX'], case_insensitive=True)

        # See ~/cogs/ for more info
        self.loaded_cogs = [
                'cogs.Events',
                'cogs.Fun',
                'cogs.Admin',
                'cogs.Gold',
                'cogs.Config',
                'cogs.GoldHandler',
#               'cogs.Twitter',
                'cogs.Welcome',
#               'cogs.Twitch'
        ]

        self.start_time = datetime.utcnow()
        self.cache = set()

        self.gold_channel = 0
        self.gold_db = GoldDatabaseHandler("utils/resources/database.db")

        self.startup()

    def startup(self):
        for cog in self.loaded_cogs:
            print(f'Loaded extension {cog}')
            self.load_extension(cog)
def main():
    bot = PotatoBot()

    path = os.getcwd()
    initialize_logging(path)

    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print('Closing bot, bye! =)')
    except Exception as e:
        print('To run this bot you must set environment variable DISCORD_TOKEN to your Bot\'s token.')
        print(e)

if __name__ == '__main__':
    main()

