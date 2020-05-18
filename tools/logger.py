import logging
import logging.handlers
import sys
import codecs
from utils.helper import create_folder

class StdoutLogger(object):
    '''Console logger'''
    def __init__(self, log):
        self.log = log
        self.console = sys.__stdout__
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    def write(self, message):
        self.console.write(message)
        if not message.isspace():
            self.log(message)

    def flush(self):
        pass

def set_console_logging(path, formatter):
    console_logger = logging.getLogger('console')
    console_logger.setLevel(logging.DEBUG)

    console_handler = logging.FileHandler(filename=path+'console.log', encoding='UTF-8', mode='a')
    console_handler.setFormatter(formatter)

    console_logger.addHandler(console_handler)

    sys.stdout = StdoutLogger(console_logger.info)

def set_exception_logging(path, formatter):
    exception_logging = logging.getLogger('exceptions')
    exception_logging.setLevel(logging.ERROR)

    exception_handler = logging.FileHandler(filename=path+'exceptions.log', encoding='UTF-8')
    exception_handler.setFormatter(formatter)

    exception_logging.addHandler(exception_handler)

    def log_exception(exc_type, exc_value, exc_traceback):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        exception_logging.exception("Exception\n", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = log_exception

def set_discord_logging(path, formatter):
    discord_logging = logging.getLogger('discord')
    discord_logging.setLevel(logging.INFO)
    
    discord_handler = logging.handlers.TimedRotatingFileHandler(filename=path+'/discord/discord.log', when='midnight')
    discord_handler.setFormatter(formatter)

    discord_logging.addHandler(discord_handler)

def initialize_logging(path):

    path += '/logs/'

    create_folder(path)
    create_folder(path + 'discord')

    formatter = logging.Formatter("%(asctime)s: %(message)s")

    set_console_logging(path, formatter)
    set_exception_logging(path, formatter)
    set_discord_logging(path, formatter)

