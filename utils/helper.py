from discord.ext import commands
from utils.config import GLOBAL as cfg
from utils.GoldEmbed import GoldEmbed

import re
import unicodedata

def make_message(emoji, count, channel, username):
    msg = f'{emoji} **{count}** em {channel.mention}' 
    msg += '' if username == None else ' por ' + username
    return msg

def get_message_info(reaction):
    return cfg['DEFAULT_GOLD_EMOJI'], reaction.count, reaction.message.channel

async def remove_special_chars(string):
    """https://gist.github.com/boniattirodrigo/67429ada53b7337d2e79"""

    nfkd = unicodedata.normalize('NFKD', string)
    no_accents = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', no_accents).lower()

async def send_gold_message(reaction, to_channel, _embed, gold_files):
    emoji, count, from_channel = get_message_info(reaction)

    if not isinstance(_embed, GoldEmbed):
        user = reaction.message.author.mention
    else:
        user = None

    message = await to_channel.send(make_message(emoji, count, from_channel, user), embed=_embed, files=gold_files)
    return message

async def edit_gold_message(message, reaction):

    emoji, count, from_channel = get_message_info(reaction)

    _embed = message.Embeds[0]

    if not isinstance(_embed, GoldEmbed):
        user = reaction.message.author.mention
    else:
        user = None

    new_content = make_message(emoji, count, from_channel, user) 

    await message.edit(content=new_content)
