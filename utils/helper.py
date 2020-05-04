from discord.ext import commands
from utils.config import GLOBAL as cfg

import re
import unicodedata

def make_message(emoji, count, channel):
    return f'{emoji} **{count}** in {channel.mention}'

def get_message_info(reaction):
    return cfg['DEFAULT_GOLD_EMOJI'], reaction.count, reaction.message.channel

async def remove_special_chars(string):
    """https://gist.github.com/boniattirodrigo/67429ada53b7337d2e79"""

    nfkd = unicodedata.normalize('NFKD', string)
    no_accents = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', no_accents).lower()

async def send_gold_message(reaction, to_channel, gold_embed):
    emoji, count, from_channel = get_message_info(reaction)

    message = await to_channel.send(make_message(emoji, count, from_channel), embed=gold_embed)
    
    return message

async def edit_gold_message(message, reaction):

    emoji, count, from_channel = get_message_info(reaction)

    new_content = make_message(emoji, count, from_channel) 

    await message.edit(content=new_content)
