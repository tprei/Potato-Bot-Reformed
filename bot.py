import discord
import logging
import os, sys

TOKEN = os.environ.get('DISCORD_TOKEN')
LOG_VERBOSITY = 0

def parseOptions():
    verbosity = int(sys.argv[1])

    LOG_VERBOSITY = verbosity

    if LOG_VERBOSITY == 1:
        logging.basicConfig(level=logging.DEBUG)
    elif LOG_VERBOSITY == 2:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parseOptions()


