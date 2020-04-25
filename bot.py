from datetime import datetime

from discord.ext import commands
import logging

import os, sys
from utils.config import GLOBAL as cfg

LOG_VERBOSITY = 0
TOKEN = os.environ.get('DISCORD_TOKEN')

class PotatoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cfg['COMMANDS_PREFIX'])

        # See ~/cogs/ for more info
        self.loaded_cogs = [
                'cogs.Events',
                'cogs.Fun',
                'cogs.Admin',
                'cogs.Gold',
                'cogs.Config'
        ]

        self.start_time = datetime.utcnow()

        self.gold_channel = 0
        self.gold_ids = {}

        self.startup()

    def startup(self):
        for cog in self.loaded_cogs:
            try:
                self.load_extension(cog)
                print(f'Loaded cog {cog}')
            except Exception as e:
                print(e)

def parseOptions():
    verbosity = int(sys.argv[1])

    LOG_VERBOSITY = verbosity

    if LOG_VERBOSITY == 1:
        logging.basicConfig(level=logging.DEBUG)
    elif LOG_VERBOSITY == 2:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.WARNING)

def main():
    parseOptions()

    bot = PotatoBot()
    bot.run(TOKEN)

if __name__ == '__main__':
    main()

